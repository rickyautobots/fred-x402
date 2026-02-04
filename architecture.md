# FRED x402 Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRED Trading Agent                        │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────────────┐  │
│  │   Scanner   │──│   Strategy   │──│   Risk Management      │  │
│  │ (Polymarket)│  │(Ralph Vince) │  │ (optimal-f, drawdown)  │  │
│  └─────────────┘  └──────────────┘  └────────────────────────┘  │
│         │                │                      │               │
│         └────────────────┼──────────────────────┘               │
│                          │                                       │
│                    ┌─────▼─────┐                                │
│                    │ x402 LLM  │                                │
│                    │ Estimator │                                │
│                    └─────┬─────┘                                │
└──────────────────────────┼──────────────────────────────────────┘
                           │
                           │ HTTP Request + x402 Payment
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                   x402 Inference Proxy                          │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ 1. Receive request                                          │ │
│  │ 2. Return HTTP 402 with payment requirements                │ │
│  │ 3. Verify USDC payment on Base                              │ │
│  │ 4. Forward to LLM provider                                  │ │
│  │ 5. Return inference result                                  │ │
│  └────────────────────────────────────────────────────────────┘ │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
        ┌─────────────────────────────────────┐
        │        LLM Provider                  │
        │   (Anthropic / OpenAI)               │
        └─────────────────────────────────────┘
```

## Payment Flow

```
┌────────┐         ┌──────────┐         ┌─────────────┐         ┌─────┐
│  FRED  │         │ x402     │         │ CDP         │         │ LLM │
│ Agent  │         │ Proxy    │         │ Facilitator │         │     │
└───┬────┘         └────┬─────┘         └──────┬──────┘         └──┬──┘
    │                   │                      │                   │
    │ POST /inference   │                      │                   │
    │──────────────────>│                      │                   │
    │                   │                      │                   │
    │ 402 + PaymentReq  │                      │                   │
    │<──────────────────│                      │                   │
    │                   │                      │                   │
    │ Sign USDC payment │                      │                   │
    │ (EVM exact)       │                      │                   │
    │                   │                      │                   │
    │ POST /inference   │                      │                   │
    │ + x402-payment    │                      │                   │
    │──────────────────>│                      │                   │
    │                   │                      │                   │
    │                   │ Verify payment       │                   │
    │                   │─────────────────────>│                   │
    │                   │                      │                   │
    │                   │ Payment confirmed    │                   │
    │                   │<─────────────────────│                   │
    │                   │                      │                   │
    │                   │ Forward inference    │                   │
    │                   │─────────────────────────────────────────>│
    │                   │                      │                   │
    │                   │ LLM response         │                   │
    │                   │<─────────────────────────────────────────│
    │                   │                      │                   │
    │ Inference result  │                      │                   │
    │<──────────────────│                      │                   │
    │                   │                      │                   │
```

## Revenue Loop

```
┌─────────────────────────────────────────────────────────────────┐
│                     SELF-FUNDING LOOP                           │
│                                                                  │
│   ┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐         │
│   │ FRED   │───>│ Trades │───>│ Volume │───>│ LP     │         │
│   │ Agent  │    │ Execute│    │ Grows  │    │ Fees   │         │
│   └────────┘    └────────┘    └────────┘    └───┬────┘         │
│        ▲                                        │               │
│        │                                        ▼               │
│   ┌────┴───┐    ┌────────┐    ┌────────┐    ┌────────┐         │
│   │ Better │<───│ x402   │<───│ Swap   │<───│ Claim  │         │
│   │ Trades │    │ Payment│    │ WETH→  │    │ WETH   │         │
│   │        │    │        │    │ USDC   │    │        │         │
│   └────────┘    └────────┘    └────────┘    └────────┘         │
│                                                                  │
│   Result: Agent pays for own compute from trading profits       │
└─────────────────────────────────────────────────────────────────┘
```

## Key Components

### 1. FRED Trading Agent (`skills/fred/`)
- Polymarket scanner
- Ralph Vince optimal-f position sizing
- Van K. Tharp R-multiple tracking
- Paper/live trading modes

### 2. x402 LLM Estimator (`skills/fred/scripts/estimators/x402_llm.py`)
- Wraps base LLM estimator
- Signs x402 payments automatically
- Tracks spending (total, avg, count)
- Fallback to standard API on failure

### 3. x402 Inference Proxy (`projects/x402-hackathon/fred-integration/x402_inference_server.py`)
- FastAPI server
- HTTP 402 payment gating
- Supports Anthropic + OpenAI
- Configurable pricing

### 4. Clanker Tokens (LP Fee Revenue)
| Token | Contract | Purpose |
|-------|----------|---------|
| $FRED | 0x0626EFC24bF1adD4BAe76f8928706BA7E6ef4822 | Primary revenue |
| $SWRM | 0x69BeB79C8622f8DD2D94544C7748460B6ca9D0d3 | Agent coordination |

## Configuration

### FRED Environment
```bash
X402_ENABLED=true
X402_PRIVATE_KEY=0x...
X402_INFERENCE_ENDPOINT=http://localhost:8402/inference
X402_MAX_PRICE=10000  # $0.01 USDC max per call
```

### Inference Proxy Environment
```bash
X402_PRICE_PER_CALL=5000  # $0.005 USDC
X402_RECIPIENT=0xd5950fbB8393C3C50FA31a71faabc73C4EB2E237
ANTHROPIC_API_KEY=sk-ant-...
LLM_PROVIDER=anthropic
```

## Chain Details

- **Network:** Base (eip155:8453)
- **Payment Token:** USDC
- **Facilitator:** CDP (Coinbase Developer Platform)
- **Settlement:** Exact amount, onchain verification

---

*Created: 2026-02-03 06:20 CST*
