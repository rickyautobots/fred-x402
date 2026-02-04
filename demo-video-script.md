# FRED x402 Demo Video Script

**Target: 2-3 minutes**
**Format:** Screen recording with voiceover

---

## Intro (15 sec)

**Visual:** FRED logo + x402 badge

**Script:**
"Meet FRED — an autonomous AI trading agent that pays for its own intelligence through Coinbase x402 micropayments. Today I'll show you how FRED self-funds its operations on the Base network."

---

## Problem Statement (20 sec)

**Visual:** Diagram showing AI agent → API costs → bank account dependency

**Script:**
"AI agents need compute, LLM inference, data feeds. Right now, they depend on human-funded API keys. That's a bottleneck — agents can't operate autonomously if they can't pay their own bills."

---

## Solution (20 sec)

**Visual:** x402 payment flow diagram

**Script:**
"x402 changes this. HTTP 402 micropayments let agents pay per-request with USDC. No subscriptions, no human intervention. The agent earns, the agent spends."

---

## Demo: FRED Self-Funding Loop (90 sec)

### Part 1: FRED Scanning Markets (20 sec)

**Visual:** Terminal showing FRED scanning Polymarket

**Script:**
"FRED continuously scans Polymarket for trading opportunities. When it finds a promising market, it needs to estimate the true probability..."

### Part 2: x402 Payment for Inference (30 sec)

**Visual:** Terminal logs showing:
1. x402 request to inference endpoint
2. HTTP 402 response with payment requirement
3. USDC payment signed and sent
4. Inference response received

**Script:**
"Here's where x402 kicks in. FRED sends an inference request. The server responds with HTTP 402 — payment required. FRED signs a USDC payment, server verifies it, and returns the LLM probability estimate. That's $0.005 for a Claude inference call, paid instantly on Base."

### Part 3: Trade Execution (20 sec)

**Visual:** FRED executing trade based on probability

**Script:**
"With the probability estimate, FRED applies Ralph Vince's optimal-f algorithm to size the position, then executes the trade. No human approval needed."

### Part 4: Revenue Loop (20 sec)

**Visual:** Diagram: Trades → LP Fees → Claim WETH → Swap USDC → x402 payments → More inference

**Script:**
"The magic: FRED earns LP fees from Clanker tokens. Those fees get claimed as WETH, swapped to USDC, and fund more x402 inference calls. Self-sustaining AI."

---

## Technical Stack (15 sec)

**Visual:** Code snippets / architecture diagram

**Script:**
"Built with FastAPI for the x402 inference proxy, the Coinbase x402 Python SDK for payments, and FRED's existing Polymarket integration. All running on Base mainnet."

---

## Conclusion (15 sec)

**Visual:** FRED stats + wallet balance

**Script:**
"FRED proves AI agents can pay for their own compute through onchain micropayments. No more API key dependencies. This is the future of autonomous AI — agents that earn, spend, and compound on their own."

---

## Call to Action (10 sec)

**Visual:** GitHub link + @coinbaseDev mention

**Script:**
"Code is open source. Link in description. Follow @coinbaseDev for more x402 projects."

---

## Recording Checklist

- [ ] Clean terminal (no personal info)
- [ ] Fund wallet with test USDC (~$1)
- [ ] Run FRED in verbose mode
- [ ] Capture x402 payment logs clearly
- [ ] Show wallet balance before/after
- [ ] Record audio separately for clarity
- [ ] Keep under 3 minutes

## Assets Needed

- [ ] FRED logo
- [ ] x402 logo
- [ ] Architecture diagram (Figma or Mermaid)
- [ ] Payment flow animation (optional)

---

*Created: 2026-02-03 06:15 CST*
