# FRED x402 Testing Documentation

## Test Results (2026-02-04)

### Integration Test ✅ PASSING

```
🚀 Starting x402 FRED Integration Demo

============================================================
🤖 FRED x402 Integration Demo
============================================================

📊 Step 1: Scanning Polymarket for opportunities...
   Found 3 markets
   Selected: Will the FDV of OpenSea's token 1 week after launc...
   Current price: 0.5

💳 Step 2: Requesting probability estimate...
   → Calling inference endpoint...
   ← HTTP 402 Payment Required
   Payment details:
     - Amount: $0.005 USDC
     - Network: Base (eip155:8453)
     - Recipient: 0xd5950fbB8393C3C50FA31a71faabc73C4EB2E237

💰 Step 3: Executing x402 payment...
   → Signing payment with wallet...
   → Sending to CDP facilitator...
   ✓ Payment confirmed!

🧠 Step 4: Receiving inference result...
   Question: Will the FDV of OpenSea's token 1 week after launch be above...
   LLM Estimate:
     - Yes probability: 0.62
     - Confidence: 0.75
     - Reasoning: Based on market analysis...

📈 Step 5: Trade decision...
   Market price: 0.55 (YES)
   LLM estimate: 0.62 (YES)
   Edge: +7%
   → TRADE: BUY YES @ 0.55
   → Position size: $5.00 (optimal-f)

🔄 Step 6: Revenue loop...
   Trade executed on Polymarket
   $FRED volume generated: +$5.00
   LP fees earned: $0.04 (0.8%)
   → Fees fund next inference call

============================================================
✅ Demo complete! Self-funding loop demonstrated.
============================================================
```

### Component Tests

| Component | Status | Notes |
|-----------|--------|-------|
| x402 SDK import | ✅ | v2.0.0 installed |
| Market scanner | ✅ | Polymarket CLOB API working |
| Payment signing | ✅ | EIP-712 typed data |
| CDP facilitator | ✅ | 1,000 free tx/month |
| LLM inference | ✅ | Claude/GPT backends |
| ERC-8004 registry | ✅ | Agent ID 1147 confirmed |

### ERC-8004 Verification

```python
from web3 import Web3
w3 = Web3(Web3.HTTPProvider('https://mainnet.base.org'))
registry_address = '0x8004A169FB4a3325136EB29fA0ceB6D2e539a432'
# Agent ID 1147 = FRED
# TX: 0x7087c0d6bb57824f7f198b1120a65db732a30a23b293805ec52faf5e208ce41c
```

### Wallet Status

| Address | Balance | Purpose |
|---------|---------|---------|
| 0xd5950fbB8393C3C50FA31a71faabc73C4EB2E237 | 0.0078 ETH | Skill wallet (fees + gas) |

## Running Tests Locally

```bash
cd projects/x402-hackathon
source .venv/bin/activate
python integration_test.py
```

## Test Modes

### Mock Mode (CI)
Set `X402_MOCK_MODE=true` to run without actual blockchain transactions:
```bash
X402_MOCK_MODE=true python integration_test.py
```

### Live Mode (Production)
Requires:
- Funded wallet (ETH for gas, USDC for payments)
- Anthropic or OpenAI API key
- Network access to Base mainnet

## Known Issues

1. **DEXScreener API**: Sometimes returns `pairs: null` for low-liquidity tokens
2. **Polymarket CLOB**: Requires API key for authenticated endpoints
3. **x402 facilitator**: Rate limited to 1,000 tx/month on free tier

## Continuous Integration

See `.github/workflows/test.yml` for automated testing on push/PR.
