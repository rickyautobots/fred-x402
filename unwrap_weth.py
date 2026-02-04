#!/usr/bin/env python3
"""Unwrap WETH to ETH"""

from web3 import Web3

RPC = "https://mainnet.base.org"
SKILL_WALLET = "0xd5950fbB8393C3C50FA31a71faabc73C4EB2E237"
SKILL_KEY = "REDACTED_KEY"
WETH = "0x4200000000000000000000000000000000000006"

w3 = Web3(Web3.HTTPProvider(RPC))

# WETH withdraw ABI
WETH_ABI = [{"constant":False,"inputs":[{"name":"wad","type":"uint256"}],"name":"withdraw","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"}]

weth = w3.eth.contract(address=WETH, abi=WETH_ABI)

# Get WETH balance
weth_balance = w3.eth.call({
    'to': WETH,
    'data': '0x70a08231' + SKILL_WALLET[2:].zfill(64).lower()
})
weth_amount = int.from_bytes(weth_balance, 'big')

print(f"WETH balance: {w3.from_wei(weth_amount, 'ether'):.6f}")
print(f"ETH balance:  {w3.from_wei(w3.eth.get_balance(SKILL_WALLET), 'ether'):.6f}")

if weth_amount == 0:
    print("No WETH to unwrap")
    exit(0)

# Build unwrap tx
gas_price = w3.eth.gas_price
nonce = w3.eth.get_transaction_count(SKILL_WALLET)

tx = weth.functions.withdraw(weth_amount).build_transaction({
    'from': SKILL_WALLET,
    'nonce': nonce,
    'gas': 50000,  # WETH withdraw is cheap
    'gasPrice': gas_price,
    'chainId': 8453
})

# Sign and send
signed = w3.eth.account.sign_transaction(tx, SKILL_KEY)
tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)

print(f"\nUnwrapping {w3.from_wei(weth_amount, 'ether'):.6f} WETH → ETH")
print(f"TX: https://basescan.org/tx/{tx_hash.hex()}")

receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Confirmed in block {receipt['blockNumber']}")
print(f"\nNew ETH balance: {w3.from_wei(w3.eth.get_balance(SKILL_WALLET), 'ether'):.6f}")
