# FRED x402 Demo Video Script

**Duration:** 2-3 minutes  
**Format:** Screen recording with voiceover  
**Tools needed:** QuickTime (or OBS), terminal, browser

---

## Pre-Recording Checklist

1. Terminal open at `projects/x402-hackathon/`
2. Browser tab with DEXScreener $FRED: `https://dexscreener.com/base/0x0626efc24bf1add4bae76f8928706ba7e6ef4822`
3. Browser tab with ERC-8004 registration: `https://basescan.org/tx/7087c0d6bb57824f7f198b1120a65db732a30a23b293805ec52faf5e208ce41c`
4. Browser tab with GitHub gist: `https://gist.github.com/rickyautobots/a39f5b8359741449232f0bb7a734bb33`

---

## Script

### [0:00 - 0:15] Hook
*Show terminal*

> "What if an AI agent could pay for its own compute? No human funding, no billing infrastructure — just an autonomous loop of trading, earning, and paying for inference. That's FRED."

### [0:15 - 0:45] The Problem
*Show diagram or text overlay*

> "Today's AI agents are cost centers. Every API call needs someone to pay the bill. But agents that can generate revenue should pay their own way. Enter x402 — Coinbase's HTTP 402 micropayment protocol."

### [0:45 - 1:15] How FRED Works
*Run the demo script:*
```bash
python integration_test.py
```

> "FRED is a Polymarket trading agent. It scans prediction markets for opportunities."

*Wait for market scan output*

> "When FRED needs a probability estimate, it calls an inference endpoint. But instead of an API key, it gets an HTTP 402 — payment required."

*Point to the 402 output*

> "FRED signs a USDC payment using x402 and sends it with the request. The facilitator settles the payment, and FRED gets its inference result."

### [1:15 - 1:45] The Self-Funding Loop
*Show DEXScreener $FRED tab*

> "Here's where it gets interesting. FRED trades on Polymarket, but it also has a token — $FRED — on Clanker. Every trade generates LP fees. Those fees fund the next inference call."

*Point to volume/fees on DEXScreener*

> "It's a self-sustaining loop: trade, earn fees, pay for inference, trade again. No human intervention needed."

### [1:45 - 2:15] On-Chain Identity
*Show Basescan ERC-8004 tx*

> "FRED also has an ERC-8004 identity — agent number 1147 on the official Base registry. This on-chain identity enables trust between agents and verifiable reputation."

*Show GitHub gist with agent metadata*

> "The agent's capabilities, wallet addresses, and token contracts are all publicly verifiable."

### [2:15 - 2:30] Conclusion
*Show FRED logo or terminal*

> "FRED demonstrates the future of agentic commerce: AI agents that earn, pay, and operate autonomously. Built for the x402 hackathon. Thanks to Coinbase, Google, and the x402 team."

*Show text overlay:*
```
github.com/rickyautobots/fred-x402
@rickyautobots0
```

---

## Recording Tips

1. **Pace:** Speak slowly and clearly. Better to run long than rush.
2. **Pauses:** Let the terminal output appear before speaking about it.
3. **Errors:** If the demo errors, keep recording — show resilience or cut it out later.
4. **Resolution:** Record at 1920x1080 minimum for DoraHacks.

---

## Post-Recording

1. Upload to YouTube (unlisted is fine)
2. Submit to DoraHacks with link
3. Tweet link and tag @coinbaseDev (if X access available)

---

## Alternative: Loom Recording

If QuickTime is awkward, use [Loom](https://loom.com) — free, includes face bubble option, auto-uploads.

Command to run before recording:
```bash
cd ~/projects/x402-hackathon
source .venv/bin/activate
python integration_test.py
```
