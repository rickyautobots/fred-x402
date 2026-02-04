#!/usr/bin/env python3
"""
FRED ERC-8004 Integration
Register FRED trading agent on Base mainnet ERC-8004 Identity Registry
"""

import json
import os
from web3 import Web3
from eth_account import Account

# Base Mainnet ERC-8004 Contracts (official)
IDENTITY_REGISTRY = "0x8004A169FB4a3325136EB29fA0ceB6D2e539a432"
REPUTATION_REGISTRY = "0x8004BAa17C55a88189AE136b182e5fdA19dE9b63"

# Base Mainnet RPC
BASE_RPC = "https://mainnet.base.org"

# FRED Registration File URI (to be hosted)
FRED_REGISTRATION_URI = "https://raw.githubusercontent.com/rickyautobots/fred-agent/main/registration.json"

# Identity Registry ABI (minimal for registration)
IDENTITY_ABI = [
    {
        "inputs": [{"name": "to", "type": "address"}, {"name": "tokenURI", "type": "string"}],
        "name": "register",
        "outputs": [{"name": "tokenId", "type": "uint256"}],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"name": "tokenId", "type": "uint256"}],
        "name": "tokenURI",
        "outputs": [{"name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"name": "owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"name": "owner", "type": "address"}, {"name": "index", "type": "uint256"}],
        "name": "tokenOfOwnerByIndex",
        "outputs": [{"name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    }
]

# Reputation Registry ABI (minimal)
REPUTATION_ABI = [
    {
        "inputs": [
            {"name": "agentId", "type": "uint256"},
            {"name": "score", "type": "int8"},
            {"name": "feedbackURI", "type": "string"}
        ],
        "name": "submitFeedback",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"name": "agentId", "type": "uint256"}],
        "name": "getAverageScore",
        "outputs": [{"name": "", "type": "int256"}],
        "stateMutability": "view",
        "type": "function"
    }
]


def create_registration_file():
    """Create FRED's ERC-8004 registration file"""
    registration = {
        "$schema": "https://erc-8004.org/schemas/registration/v1.json",
        "name": "FRED",
        "description": "Autonomous Polymarket trading agent with x402 micropayment integration. Uses Ralph Vince optimal-f position sizing and LLM probability estimation.",
        "version": "1.0.0",
        "capabilities": [
            {
                "type": "trading",
                "markets": ["polymarket"],
                "features": ["probability_estimation", "position_sizing", "autonomous_execution"]
            },
            {
                "type": "x402_payments",
                "supported": True,
                "payment_address": "0xd5950fbB8393C3C50FA31a71faabc73C4EB2E237"
            }
        ],
        "endpoints": {
            "inference": "https://fred.openclaw.ai/api/inference",
            "status": "https://fred.openclaw.ai/api/status"
        },
        "owner": "0xd5950fbB8393C3C50FA31a71faabc73C4EB2E237",
        "contacts": {
            "github": "https://github.com/rickyautobots/fred-agent",
            "x": "https://x.com/rickyautobots0"
        },
        "tokens": {
            "FRED": {
                "chain": "base",
                "address": "0x0626EFC24bF1adD4BAe76f8928706BA7E6ef4822",
                "type": "clanker_lp"
            }
        }
    }
    return registration


def register_agent(private_key: str, registration_uri: str):
    """Register FRED on Base ERC-8004 Identity Registry"""
    w3 = Web3(Web3.HTTPProvider(BASE_RPC))
    account = Account.from_key(private_key)
    
    identity = w3.eth.contract(address=IDENTITY_REGISTRY, abi=IDENTITY_ABI)
    
    # Check if already registered
    balance = identity.functions.balanceOf(account.address).call()
    if balance > 0:
        token_id = identity.functions.tokenOfOwnerByIndex(account.address, 0).call()
        print(f"Already registered! Agent ID: {token_id}")
        return token_id
    
    # Build registration transaction
    tx = identity.functions.register(
        account.address,
        registration_uri
    ).build_transaction({
        'from': account.address,
        'nonce': w3.eth.get_transaction_count(account.address),
        'gas': 200000,
        'gasPrice': w3.eth.gas_price,
        'chainId': 8453  # Base mainnet
    })
    
    # Sign and send
    signed = account.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    
    print(f"Registration tx: {tx_hash.hex()}")
    
    # Wait for confirmation
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Confirmed in block {receipt['blockNumber']}")
    
    # Get token ID from logs
    # The Transfer event logs the new token ID
    return receipt


def check_registration(address: str):
    """Check if an address has a registered agent"""
    w3 = Web3(Web3.HTTPProvider(BASE_RPC))
    identity = w3.eth.contract(address=IDENTITY_REGISTRY, abi=IDENTITY_ABI)
    
    balance = identity.functions.balanceOf(address).call()
    print(f"Address {address} has {balance} registered agent(s)")
    
    if balance > 0:
        for i in range(balance):
            token_id = identity.functions.tokenOfOwnerByIndex(address, i).call()
            uri = identity.functions.tokenURI(token_id).call()
            print(f"  Agent #{token_id}: {uri}")
    
    return balance


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        # Check our wallet's registration status
        check_registration("0xd5950fbB8393C3C50FA31a71faabc73C4EB2E237")
    elif len(sys.argv) > 1 and sys.argv[1] == "registration":
        # Print registration file
        reg = create_registration_file()
        print(json.dumps(reg, indent=2))
    else:
        print("Usage:")
        print("  python fred-8004-integration.py check        # Check registration status")
        print("  python fred-8004-integration.py registration # Print registration JSON")
        print("")
        print("To register, set PRIVATE_KEY env var and call register_agent()")
