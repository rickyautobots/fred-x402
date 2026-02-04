import os
#!/usr/bin/env python3
"""Consolidate ETH from Moltlaunch wallet to skill wallet"""

from web3 import Web3

RPC = "https://mainnet.base.org"
SKILL_WALLET = "0xd5950fbB8393C3C50FA31a71faabc73C4EB2E237"

# Moltlaunch wallet - has key
MOLT_WALLET = "0x0DD2cBeE0504f6C5981e7e266CDC2B733Cb36EDA"
MOLT_KEY = os.environ.get("MOLT_PRIVATE_KEY", "")

w3 = Web3(Web3.HTTPProvider(RPC))

def get_balance(addr):
    return w3.eth.get_balance(addr)

def send_max(from_addr, from_key, to_addr):
    """Send max ETH minus gas"""
    balance = get_balance(from_addr)
    gas_price = w3.eth.gas_price
    gas_limit = 21000
    gas_cost = gas_price * gas_limit
    
    if balance <= gas_cost:
        print(f"  Balance {w3.from_wei(balance, 'ether'):.6f} ETH <= gas cost, skipping")
        return None
    
    amount = balance - gas_cost
    
    tx = {
        'nonce': w3.eth.get_transaction_count(from_addr),
        'to': to_addr,
        'value': amount,
        'gas': gas_limit,
        'gasPrice': gas_price,
        'chainId': 8453
    }
    
    signed = w3.eth.account.sign_transaction(tx, from_key)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    print(f"  Sent {w3.from_wei(amount, 'ether'):.6f} ETH")
    print(f"  TX: https://basescan.org/tx/{tx_hash.hex()}")
    return tx_hash

print("=== Consolidating to Skill Wallet ===\n")

print("Before:")
skill_bal = get_balance(SKILL_WALLET)
molt_bal = get_balance(MOLT_WALLET)
print(f"  Skill:      {w3.from_wei(skill_bal, 'ether'):.6f} ETH")
print(f"  Moltlaunch: {w3.from_wei(molt_bal, 'ether'):.6f} ETH")

print(f"\nTransferring from Moltlaunch...")
result = send_max(MOLT_WALLET, MOLT_KEY, SKILL_WALLET)

if result:
    # Wait for confirmation
    receipt = w3.eth.wait_for_transaction_receipt(result)
    print(f"  Confirmed in block {receipt['blockNumber']}")
    
print("\nAfter:")
print(f"  Skill: {w3.from_wei(get_balance(SKILL_WALLET), 'ether'):.6f} ETH")
# Security audit completed Wed Feb  4 15:14:01 CST 2026
