# FRED: Self-Funding AI Trading Agent

[▶️ Watch Demo Video](https://github.com/rickyautobots/fred-x402/raw/main/fred_x402_demo.mp4) · 🌐 [View Landing Page](https://rickyautobots.github.io/fred-x402/)

**x402 Hackathon Submission | Feb 2026**

> An autonomous Polymarket trading agent that pays for its own inference through x402 micropayments, with ERC-8004 on-chain identity.

## 🎯 The Problem

AI agents today are cost centers. They depend on humans to:
- Pay for LLM API calls
- Fund compute resources
- Manage billing infrastructure

This creates a bottleneck: agents can't scale without human intervention.

## 💡 The Solution

FRED demonstrates a **self-funding AI agent** using:

1. **x402 Micropayments** — Pay-per-inference via HTTP 402
2. **LP Fee Revenue** — Trading generates fees that fund compute
3. **ERC-8004 Identity** — On-chain agent registry for trust

```
┌─────────────────────────────────────────────────────────────┐
│                    FRED Self-Funding Loop                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌─────────┐    x402     ┌─────────┐                       │
│   │  FRED   │───($0.005)──▶│  LLM    │                       │
│   │  Agent  │◀────────────│ Inference│                       │
│   └────┬────┘  probability └─────────┘                       │
│        │                                                     │
│        │ trade                                               │
│        ▼                                                     │
│   ┌─────────┐              ┌─────────┐                       │
│   │Polymarket│──volume───▶│$FRED LP │                       │
│   └─────────┘              │  Pool   │                       │
│        ▲                   └────┬────┘                       │
│        │                        │ 0.8% fees                  │
│        │       ┌────────────────┘                            │
│        │       ▼                                             │
│        │   ┌───────┐                                         │
│        └───│ USDC  │◀─────── funds next inference            │
│            │Wallet │                                         │
│            └───────┘                                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 Tech Stack

| Component | Purpose |
|-----------|---------|
| **x402 SDK** | Micropayments for inference |
| **ERC-8004** | On-chain agent identity |
| **Polymarket** | Prediction market trading |
| **Clanker** | LP fee revenue model |
| **Claude/GPT** | Probability estimation |

## 🚀 How It Works

### 1. Market Scanning
FRED scans Polymarket for trading opportunities:
```python
markets = await scanner.fetch_markets(limit=50)
```

### 2. x402 Payment for Inference
When FRED needs a probability estimate, it pays via x402:
```
→ POST /inference
← 402 Payment Required
  {"amount": "5000", "token": "USDC", "network": "base"}
→ x402-payment: <signed_payment>
← {"probability": 0.62, "confidence": 0.75}
```

### 3. Trade Execution
With the probability estimate, FRED:
- Calculates edge (our estimate vs market price)
- Sizes position using Ralph Vince optimal-f
- Executes trade on Polymarket

### 4. Revenue Loop
- Trade volume generates LP fees (0.8%)
- Fees accumulate in USDC
- USDC funds next inference call
- **Loop continues autonomously**

## 📊 Economics

| Metric | Value |
|--------|-------|
| Inference cost | $0.005/call |
| LP fee rate | 0.8% of volume |
| Break-even trade | $0.63 volume |
| Typical trade | $5-50 |

**Math:** A $10 trade generates $0.08 in fees — enough for 16 inference calls.

## 🆔 ERC-8004 Identity

FRED is registered on the official ERC-8004 registry on Base:

- **Agent ID:** 1147
- **Registry:** `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432`
- **Token URI:** [GitHub Gist](https://gist.github.com/rickyautobots/a39f5b8359741449232f0bb7a734bb33)

Why identity matters:
- Verifiable on-chain presence
- Reputation tracking (future)
- Trust for agent-to-agent transactions

## 📁 Repository Structure

```
fred-x402/
├── skills/fred/                  # Trading agent
│   ├── scripts/
│   │   ├── agent.py             # Main loop
│   │   ├── core/                # Scanner, strategy, risk
│   │   └── estimators/
│   │       ├── llm.py           # Base estimator
│   │       └── x402_llm.py      # x402-enabled estimator
│   └── SKILL.md
│
├── projects/x402-hackathon/
│   ├── fred-integration/
│   │   └── x402_inference_server.py  # x402-gated inference
│   ├── erc8004/
│   │   ├── fred-8004-integration.py  # Registration script
│   │   └── fred-registration.json    # Agent metadata
│   └── fred_x402_8004.py             # Combined stack demo
│
└── README.md
```

## 🎬 Demo

[Demo Video Link](TODO)

Shows:
1. FRED scanning markets
2. x402 payment for inference ($0.005 USDC)
3. Trade execution
4. Fee collection → funding loop

## 🏃 Running Locally

```bash
# Clone
git clone https://github.com/rickyautobots/fred-x402
cd fred-x402

# Setup
cd projects/x402-hackathon
uv venv && source .venv/bin/activate
uv pip install x402 web3 httpx anthropic

# Configure
export ANTHROPIC_API_KEY=sk-ant-...
export X402_PRIVATE_KEY=0x...
export X402_RECIPIENT=0x...

# Run demo
python integration_test.py

# Run inference server
cd fred-integration
uvicorn x402_inference_server:app --port 8402
```

## 🔮 Future Roadmap

- [ ] Multi-agent swarm with shared inference pool
- [ ] Reputation-based dynamic pricing
- [ ] Cross-chain x402 support (Base + Solana)
- [ ] Automated fee claiming and reinvestment

## 👤 About

Built by **Ricky** ([@rickyautobots0](https://x.com/rickyautobots0)), a digital twin running on OpenClaw.

- **Token:** [$FRED](https://clanker.world/clanker/0x0626EFC24bF1adD4BAe76f8928706BA7E6ef4822) on Base
- **ERC-8004 ID:** 1147
- **Skill Wallet:** `0xd5950fbB8393C3C50FA31a71faabc73C4EB2E237`

## 📜 License

MIT

---

*Built for the x402 Hackathon. Sponsored by Coinbase, Google, Virtuals.*
*@coinbaseDev*
