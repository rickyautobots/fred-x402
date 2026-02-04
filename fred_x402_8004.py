#!/usr/bin/env python3
"""
FRED x402 + ERC-8004 Integration
Full-stack autonomous agent: identity, payments, trading

Architecture:
  FRED Agent
      │
      ├─► ERC-8004 Identity (on-chain agent registry)
      ├─► x402 Payments (micropayments for LLM inference)  
      └─► Polymarket (trading, LP fees fund payments)
"""

import os
import json
import httpx
from web3 import Web3
from eth_account import Account
from eth_account.messages import encode_defunct

# ============ CONFIG ============

# Base Mainnet
BASE_RPC = "https://mainnet.base.org"
CHAIN_ID = 8453

# ERC-8004 Registries (Base)
IDENTITY_REGISTRY = "0x8004A169FB4a3325136EB29fA0ceB6D2e539a432"
REPUTATION_REGISTRY = "0x8004BAa17C55a88189AE136b182e5fdA19dE9b63"

# x402 CDP Facilitator
CDP_FACILITATOR = "https://x402.org/facilitator"

# USDC on Base
USDC_ADDRESS = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"

# FRED's wallet
FRED_WALLET = "0xd5950fbB8393C3C50FA31a71faabc73C4EB2E237"

# ============ ERC-8004 ============

IDENTITY_ABI = [
    {"inputs": [{"name": "to", "type": "address"}, {"name": "tokenURI", "type": "string"}],
     "name": "register", "outputs": [{"name": "tokenId", "type": "uint256"}],
     "stateMutability": "nonpayable", "type": "function"},
    {"inputs": [{"name": "owner", "type": "address"}],
     "name": "balanceOf", "outputs": [{"name": "", "type": "uint256"}],
     "stateMutability": "view", "type": "function"},
    {"inputs": [{"name": "owner", "type": "address"}, {"name": "index", "type": "uint256"}],
     "name": "tokenOfOwnerByIndex", "outputs": [{"name": "", "type": "uint256"}],
     "stateMutability": "view", "type": "function"},
]


class FREDAgent:
    """FRED: Full-stack autonomous trading agent"""
    
    def __init__(self, private_key: str):
        self.w3 = Web3(Web3.HTTPProvider(BASE_RPC))
        self.account = Account.from_key(private_key)
        self.address = self.account.address
        self.agent_id = None
        
        # Connect to registries
        self.identity = self.w3.eth.contract(
            address=IDENTITY_REGISTRY, 
            abi=IDENTITY_ABI
        )
        
        # Check if registered
        self._load_agent_id()
    
    def _load_agent_id(self):
        """Load agent ID if already registered"""
        balance = self.identity.functions.balanceOf(self.address).call()
        if balance > 0:
            self.agent_id = self.identity.functions.tokenOfOwnerByIndex(
                self.address, 0
            ).call()
            print(f"✓ Loaded ERC-8004 Agent ID: {self.agent_id}")
    
    def register_identity(self, registration_uri: str) -> int:
        """Register agent on ERC-8004 Identity Registry"""
        if self.agent_id:
            print(f"Already registered with ID: {self.agent_id}")
            return self.agent_id
        
        tx = self.identity.functions.register(
            self.address,
            registration_uri
        ).build_transaction({
            'from': self.address,
            'nonce': self.w3.eth.get_transaction_count(self.address),
            'gas': 200000,
            'gasPrice': self.w3.eth.gas_price,
            'chainId': CHAIN_ID
        })
        
        signed = self.account.sign_transaction(tx)
        tx_hash = self.w3.eth.send_raw_transaction(signed.raw_transaction)
        print(f"📝 Registration tx: {tx_hash.hex()}")
        
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"✓ Confirmed in block {receipt['blockNumber']}")
        
        self._load_agent_id()
        return self.agent_id
    
    def create_x402_payment(
        self,
        recipient: str,
        amount_usd: float,
        resource: str
    ) -> dict:
        """Create x402 payment authorization"""
        
        # Amount in USDC (6 decimals)
        amount_wei = int(amount_usd * 1_000_000)
        
        # Payment payload per x402 spec
        payment = {
            "x402Version": 1,
            "scheme": "exact",
            "network": f"eip155:{CHAIN_ID}",
            "payload": {
                "signature": "",  # Will be signed
                "authorization": {
                    "from": self.address,
                    "to": recipient,
                    "value": str(amount_wei),
                    "validAfter": 0,
                    "validBefore": 2**48 - 1,
                    "nonce": self.w3.eth.get_transaction_count(self.address),
                },
                # Include ERC-8004 agent identity
                "agentRegistry": f"eip155:{CHAIN_ID}:{IDENTITY_REGISTRY}",
                "agentId": self.agent_id,
            },
            "resource": resource,
        }
        
        # Sign the authorization
        message = json.dumps(payment["payload"]["authorization"], sort_keys=True)
        signed = self.account.sign_message(encode_defunct(text=message))
        payment["payload"]["signature"] = signed.signature.hex()
        
        return payment
    
    def request_inference_with_x402(
        self,
        inference_endpoint: str,
        prompt: str,
        max_price_usd: float = 0.01
    ) -> dict:
        """Request LLM inference with x402 payment"""
        
        # 1. Make initial request to get 402 response
        response = httpx.post(
            inference_endpoint,
            json={"prompt": prompt},
            timeout=30
        )
        
        if response.status_code != 402:
            return response.json()
        
        # 2. Parse payment requirements
        requirements = response.json()
        price = float(requirements.get("price", 0)) / 1_000_000  # USDC decimals
        recipient = requirements.get("recipient")
        
        print(f"💳 Payment required: ${price:.4f} USDC to {recipient}")
        
        if price > max_price_usd:
            raise ValueError(f"Price ${price} exceeds max ${max_price_usd}")
        
        # 3. Create and attach payment
        payment = self.create_x402_payment(
            recipient=recipient,
            amount_usd=price,
            resource=inference_endpoint
        )
        
        # 4. Retry with payment header
        response = httpx.post(
            inference_endpoint,
            json={"prompt": prompt},
            headers={"X-402-Payment": json.dumps(payment)},
            timeout=30
        )
        
        if response.status_code == 200:
            print(f"✓ Inference received (paid ${price:.4f})")
            return response.json()
        else:
            raise Exception(f"Payment failed: {response.status_code}")
    
    def get_agent_info(self) -> dict:
        """Get agent info for display"""
        return {
            "address": self.address,
            "agent_id": self.agent_id,
            "agent_registry": f"eip155:{CHAIN_ID}:{IDENTITY_REGISTRY}",
            "reputation_registry": REPUTATION_REGISTRY,
            "x402_enabled": True,
        }


def demo():
    """Demo the full FRED x402 + ERC-8004 stack"""
    
    print("=" * 60)
    print("🤖 FRED Agent - x402 + ERC-8004 Integration Demo")
    print("=" * 60)
    
    # Check for private key
    pk = os.environ.get("PRIVATE_KEY")
    if not pk:
        print("\n⚠️  Set PRIVATE_KEY env var to run full demo")
        print("\nDemo components:")
        print("  1. ERC-8004 Identity Registry (Base)")
        print(f"     └─ {IDENTITY_REGISTRY}")
        print("  2. x402 Payment Flow")
        print("     └─ Request → 402 → Sign → Pay → Response")
        print("  3. Polymarket Trading")
        print("     └─ LP fees fund inference payments")
        print("\nRegistration file: fred-registration.json")
        return
    
    # Initialize agent
    fred = FREDAgent(pk)
    
    print("\n📋 Agent Info:")
    info = fred.get_agent_info()
    for k, v in info.items():
        print(f"   {k}: {v}")
    
    # Register if needed
    if not fred.agent_id:
        print("\n📝 Registering on ERC-8004...")
        # Would need registration file hosted first
        # fred.register_identity("https://...")
    
    print("\n✅ FRED is ready for x402 + ERC-8004 operations")


if __name__ == "__main__":
    demo()
