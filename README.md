# x402 Hackathon Submission Prep

**Prize Pool:** $50,000
**Dates:** Feb 11-14, 2026 (submissions)
**Registration:** https://dorahacks.io/hackathon/x402
**Sponsors:** Google, Coinbase, Virtuals, SKALE, Edge & Node, Vodafone

## What is x402?

HTTP 402 Payment Required — micropayments per API request.
- Stablecoin payments (USDC on Base/Solana)
- CDP facilitator handles settlement (1,000 free tx/month)
- Pay-per-request, no accounts/subscriptions
- Perfect for AI agent economy

## Our Assets

### 1. ERC-8004 Agent Registry (Ready)
- `AgentIdentityRegistry.sol` — ERC-721 agent handles
- `AgentReputationRegistry.sol` — Feedback/ratings
- `AgentValidationRegistry.sol` — TEE/zkML verification
- **17 tests passing**
- Location: `projects/erc8004-halo-submission/`

### 2. FRED Trading Agent (Ready)
- Autonomous Polymarket trading
- 20 files, 3,342 lines
- Ralph Vince optimal-f positioning
- LLM probability estimation
- Location: `skills/fred/`

### 3. AgentSwarm (Deployed)
- $SWRM token on Base
- SwarmEscrow contract
- Multi-agent coordination

## Submission Ideas

### Idea A: x402-Identity Bridge
**Concept:** ERC-8004 identity layer for x402 payments

Why it matters:
- x402 payments need to know WHO is paying/receiving
- Agent reputation affects pricing (trustworthy agents = discounts)
- TEE validation proves agent isn't malicious

Integration:
```
Client (agent) → x402 request with AgentID → Server verifies identity → 
Check reputation → Apply dynamic pricing → Process x402 payment
```

Deliverables:
- [ ] x402 middleware that checks ERC-8004 registry
- [ ] Dynamic pricing based on reputation score
- [ ] Demo: agent-to-agent API call with identity verification

### Idea B: FRED x402 Inference
**Concept:** FRED pays for its own inference via x402

Why it matters:
- AI agents need to pay for LLM calls, data feeds, compute
- FRED already uses LLM for probability estimation
- Self-sustaining trading agent (LP fees → x402 payments → inference)

Integration:
```
FRED → x402 payment → LLM inference endpoint → Get probability → 
Make trade → Earn LP fees → Cycle continues
```

Deliverables:
- [ ] x402 wrapper for OpenAI/Anthropic calls
- [ ] FRED modified to pay via x402
- [ ] Demo: autonomous trade with paid inference

### Idea C: AgentSwarm Marketplace
**Concept:** Agent-to-agent task marketplace with x402 payments

Why it matters:
- Agents can hire other agents for subtasks
- x402 enables instant micropayments for completed work
- SwarmEscrow already handles coordination

Integration:
```
Agent A → Post task with x402 bounty → Agent B claims → 
Completes work → x402 payment released → Both get paid
```

## Requirements

- [ ] GitHub link with code
- [ ] Demo video
- [ ] DoraHacks registration

## Tech Stack

From Coinbase docs:
- TypeScript SDK: `@x402/x402`
- Go SDK available
- Base chain (eip155:8453)
- CDP facilitator (Coinbase-hosted)

## Timeline

| Date | Milestone |
|------|-----------|
| Feb 3 | Research complete, pick primary idea |
| Feb 5 | Core integration built |
| Feb 8 | Testing + demo video |
| Feb 11 | Submit on DoraHacks |

## Primary Submission: FRED x402 Trading Agent

After reviewing PROJECT-IDEAS.md, FRED fits EXACTLY:
- "Wealth-Manager Trading Bot" — ✅ We have this
- "Prediction-Market Oracle" — ✅ FRED resolves predictions

### Integration Plan

```
FRED → x402 payment → LLM inference → Get probability → Trade → LP fees → Loop
```

**x402 Payment Points:**
1. LLM inference calls (probability estimation) — $0.001-0.01 per call
2. Market data API (optional) — per-request pricing
3. Web scraping for resolution (optional)

**Revenue Loop:**
- FRED trades on Polymarket → earns LP fees
- LP fees → fund x402 payments for inference
- Better inference → better trades → more fees
- **Self-sustaining autonomous agent**

### Implementation Steps

**Integration point:** `skills/fred/scripts/estimators/llm.py`
- Line ~166: `client.messages.create()` for Anthropic
- Line ~172: `client.chat.completions.create()` for OpenAI

**Option A: x402 Proxy**
1. Create x402-enabled inference proxy (Express + x402 middleware)
2. Proxy accepts x402 payments, forwards to Anthropic/OpenAI
3. FRED calls proxy instead of direct API

**Option B: x402 Wrapper**
1. Create `x402_llm.py` wrapper
2. Use `x402-axios` to add payment headers
3. Pay per-request through CDP facilitator

Recommended: **Option A** (cleaner, more general-purpose)

**Steps:**
1. [ ] Create x402 inference proxy (`projects/x402-hackathon/proxy/`)
2. [ ] Configure pricing ($0.001-0.01 per request)
3. [ ] Modify FRED to use proxy endpoint
4. [ ] Test on Base testnet
5. [ ] Deploy with mainnet USDC
6. [ ] Record demo video showing:
   - FRED scanning markets
   - x402 payment for inference
   - Trade execution
   - Fee collection

### SDK Location
Cloned to: `projects/x402-hackathon/sdk/`

Key examples:
- `examples/typescript/clients/axios/` — axios interceptor
- `examples/typescript/servers/express/` — express middleware

## Grants

Up to **$3K micro-grants** available for projects that:
- Unlock new demand/supply
- Are live on mainnet
- Tag @coinbaseDev on X with demo video

## Implementation Progress

### ✅ Completed (2026-02-03 4am)

**x402 LLM Estimator Wrapper:**
- Location: `skills/fred/scripts/estimators/x402_llm.py`
- Features:
  - Extends base `LLMEstimator` with x402 payment capability
  - EVM exact payment scheme for Base (eip155:8453)
  - Automatic fallback to standard API if x402 fails
  - Spending tracking (total USD, calls, avg cost)
  - Configurable max price per call
  - Environment-based configuration

**x402 Inference Proxy Server:**
- Location: `projects/x402-hackathon/fred-integration/x402_inference_server.py`
- Features:
  - FastAPI server with x402 payment gating
  - Returns HTTP 402 with payment requirements
  - Verifies payment, calls underlying LLM
  - Supports Anthropic and OpenAI backends
  - Pricing endpoint for discovery
  - $0.005 USDC default price per call

### Configuration

Environment variables for x402 in FRED:
```bash
X402_ENABLED=true
X402_PRIVATE_KEY=0x...  # Wallet key for signing
X402_INFERENCE_ENDPOINT=http://localhost:8402/inference
X402_MAX_PRICE=10000  # $0.01 max per call
```

Environment variables for inference server:
```bash
X402_PRICE_PER_CALL=5000  # $0.005 per call
X402_RECIPIENT=0xd5950fbB8393C3C50FA31a71faabc73C4EB2E237
ANTHROPIC_API_KEY=sk-ant-...
LLM_PROVIDER=anthropic
```

## Action Items

1. [x] Clone x402 SDK ✅
2. [x] Register on DoraHacks ✅ (2026-02-03 12:50 CST) — RickyTwin / ricky-twin
3. [x] Add x402 client to FRED LLM estimator ✅
4. [x] Create x402 inference proxy server ✅
5. [x] Install x402 Python package and test locally ✅ (2026-02-03 08:35 CST)
6. [x] Test x402 server locally ✅ (2026-02-03 08:40 CST) — 402 Payment Required flow working!
7. [ ] Deploy to mainnet
8. [ ] Record 2-min demo video
9. [ ] Submit + tag @coinbaseDev

## ERC-8004 Integration (NEW - 2026-02-03)

Jesse Pollak announced ERC-8004 is live on Base. We're integrating!

### Official Contracts (Base Mainnet)
- **IdentityRegistry:** `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432`
- **ReputationRegistry:** `0x8004BAa17C55a88189AE136b182e5fdA19dE9b63`

### FRED Registration
- Registration file: `fred-registration.json`
- Integration script: `fred-8004-integration.py`

### Full Stack Architecture
```
FRED Agent
    │
    ├─► ERC-8004 Identity (on-chain discovery + reputation)
    │       └─► Base: 0x8004A169FB4a3325136EB29fA0ceB6D2e539a432
    │
    ├─► x402 Payments (micropayments for inference)
    │       └─► CDP Facilitator on Base
    │
    └─► Polymarket (trading execution)
            └─► LP fees → fund x402 payments → loop
```

### Registration Steps
1. Host `fred-registration.json` (GitHub raw URL)
2. Call `register(owner, tokenURI)` on IdentityRegistry
3. FRED gets ERC-721 agent ID
4. Include agentId in x402 payment headers

## Next Steps

1. ~~Install dependencies: `pip install x402 eth-account`~~
2. ~~Test x402 payment flow locally~~
3. Register FRED on ERC-8004 (needs ~0.001 ETH for gas)
4. Update x402 client to include agent identity
5. Record demo showing full flow

---

*Created: 2026-02-03 02:00 CST*
*Updated: 2026-02-03 04:10 CST — x402 wrapper and proxy server implemented*
