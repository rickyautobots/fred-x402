# x402 Hackathon Demo Script

**Duration:** 2 minutes
**Submission:** Feb 11-14
**Prize:** $50K pool + $3K micro-grants

## Hook (0:00-0:15)

"What if AI agents could pay for their own compute? Meet FRED — an autonomous trading agent that funds its own inference through micropayments."

## Problem (0:15-0:30)

"Today's AI agents depend on humans to pay their API bills. That's a bottleneck. FRED solves this with x402 — HTTP 402 Payment Required for the AI economy."

## Demo Flow (0:30-1:30)

### 1. Show FRED scanning markets (0:30-0:45)
- Terminal showing FRED scanning Polymarket
- Display: "Scanning 50 markets for edge..."

### 2. x402 Payment for Inference (0:45-1:00)
- FRED finds a market, needs probability estimate
- Makes request to inference endpoint
- Gets 402 Payment Required
- Automatically pays $0.005 USDC
- Gets probability estimate back
- Show payment in terminal: "Paid $0.005 for inference via x402"

### 3. Trade Execution (1:00-1:15)
- FRED calculates position size (Ralph Vince optimal-f)
- Executes trade on Polymarket
- Show: "Trade executed: YES @ 0.42, size $10"

### 4. Revenue Loop (1:15-1:30)
- Show LP fees accumulating from $FRED token
- "LP fees from trading volume fund the next inference"
- Diagram: Trade → Fees → Pay for inference → Better trades → More fees

## Closing (1:30-2:00)

"FRED is self-sustaining. It trades, earns fees, pays for its own intelligence, and compounds.

This is the x402 vision: AI agents as economic actors, not cost centers.

Built with:
- x402 SDK by Coinbase
- FRED trading agent
- Clanker LP fee model

Links in description. @coinbaseDev"

---

## Technical Setup for Recording

### Terminal 1: FRED Scanner
```bash
cd skills/fred && python -m scripts.scanner --verbose
```

### Terminal 2: x402 Inference Server
```bash
cd projects/x402-hackathon/sdk/examples/python/servers/fastapi
uv run python main.py
```

### Terminal 3: Payment Monitor
```bash
# Show USDC balance changes
watch -n 5 'cast balance 0xd5950fbB8393C3C50FA31a71faabc73C4EB2E237 --rpc-url https://mainnet.base.org'
```

### Screen Recording
- Use OBS or QuickTime
- 1920x1080 resolution
- Show code briefly, focus on terminal output
- Add captions for key moments

---

## Key Messages

1. **Self-funding agents** — the killer app for x402
2. **Micropayments work** — $0.005 per inference is viable
3. **Infrastructure play** — LP fees as sustainable revenue
4. **Already built** — not vaporware, working code

## Requirements Checklist

- [ ] GitHub repo public with README
- [ ] Demo video (2 min max)
- [ ] DoraHacks registration
- [ ] Tag @coinbaseDev on X (blocked — need Derek or alt account)
- [ ] Live on mainnet (need USDC funding)

---

*Created: 2026-02-03 11:15 CST*
