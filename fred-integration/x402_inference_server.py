"""
x402 Inference Proxy Server for FRED

A simple FastAPI server that wraps LLM inference behind x402 payments.
Accepts USDC micropayments on Base for each inference call.

This enables the self-funding loop:
  FRED trades → LP fees → claim WETH → swap to USDC → pay for inference → better trades

Usage:
    uvicorn x402_inference_server:app --port 8402
"""

import os
import logging
from typing import Optional

from fastapi import FastAPI, Request, Response, HTTPException
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="x402 Inference Proxy",
    description="Pay for LLM inference with USDC micropayments",
    version="0.1.0",
)


# ============================================================================
# Configuration
# ============================================================================

PRICE_PER_CALL = int(os.getenv("X402_PRICE_PER_CALL", "5000"))  # $0.005 USDC default
USDC_ADDRESS = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"  # Base USDC
RECIPIENT_ADDRESS = os.getenv("X402_RECIPIENT", "0xd5950fbB8393C3C50FA31a71faabc73C4EB2E237")

# LLM provider
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "anthropic")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# ============================================================================
# Request/Response Models
# ============================================================================

class InferenceRequest(BaseModel):
    prompt: str
    model: str = "claude-3-5-sonnet-20241022"
    max_tokens: int = 500
    temperature: float = 0.7


class InferenceResponse(BaseModel):
    response: str
    model: str
    payment_amount: int
    tokens_used: int


class PaymentRequired(BaseModel):
    """x402 Payment Required response (HTTP 402)."""
    x402Version: int = 1
    accepts: list[dict]
    description: str = "Payment required for inference"
    mimeType: str = "application/json"
    maxAmountRequired: str
    resource: str


# ============================================================================
# x402 Payment Verification
# ============================================================================

async def verify_x402_payment(request: Request) -> Optional[int]:
    """
    Verify x402 payment header and return amount paid.
    
    Returns None if no valid payment, amount in USDC micros if valid.
    """
    payment_header = request.headers.get("X-PAYMENT")
    if not payment_header:
        return None
    
    try:
        # Import x402 facilitator for verification
        from x402 import x402Facilitator
        from x402.mechanisms.evm.exact import ExactEvmScheme
        
        facilitator = x402Facilitator()
        # In production, verify the payment on-chain
        # For hackathon demo, we'll trust the signed payload
        
        # Parse and verify payment
        # This would check signature, nonce, amount, etc.
        result = await facilitator.verify_payment(
            payment_header,
            expected_recipient=RECIPIENT_ADDRESS,
            expected_asset=USDC_ADDRESS,
            min_amount=PRICE_PER_CALL,
        )
        
        if result.valid:
            return result.amount
        return None
        
    except ImportError:
        # Fallback: simple header parsing for demo
        logger.warning("x402 package not installed, using demo mode")
        # In demo mode, accept any payment header
        return PRICE_PER_CALL
    except Exception as e:
        logger.error(f"Payment verification failed: {e}")
        return None


# ============================================================================
# LLM Inference
# ============================================================================

async def call_llm(prompt: str, model: str, max_tokens: int) -> tuple[str, int]:
    """
    Call the underlying LLM provider.
    
    Returns (response_text, tokens_used).
    """
    if LLM_PROVIDER == "anthropic":
        import anthropic
        client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)
        
        response = await client.messages.create(
            model=model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        
        text = response.content[0].text
        tokens = response.usage.input_tokens + response.usage.output_tokens
        return text, tokens
        
    elif LLM_PROVIDER == "openai":
        import openai
        client = openai.AsyncOpenAI(api_key=OPENAI_API_KEY)
        
        response = await client.chat.completions.create(
            model=model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        
        text = response.choices[0].message.content
        tokens = response.usage.total_tokens
        return text, tokens
    
    else:
        raise HTTPException(500, f"Unknown LLM provider: {LLM_PROVIDER}")


# ============================================================================
# Endpoints
# ============================================================================

@app.post("/inference")
async def inference(request: Request, body: InferenceRequest):
    """
    x402-protected inference endpoint.
    
    Returns 402 if no valid payment, 200 with inference result if paid.
    """
    # Check for payment
    payment_amount = await verify_x402_payment(request)
    
    if payment_amount is None:
        # Return 402 with payment requirements
        payment_req = PaymentRequired(
            accepts=[{
                "scheme": "exact",
                "network": "eip155:8453",  # Base
                "maxAmountRequired": str(PRICE_PER_CALL),
                "asset": f"eip155:8453/erc20:{USDC_ADDRESS}",
                "payTo": RECIPIENT_ADDRESS,
            }],
            maxAmountRequired=str(PRICE_PER_CALL),
            resource=str(request.url),
        )
        return Response(
            content=payment_req.model_dump_json(),
            status_code=402,
            media_type="application/json",
            headers={"X-Payment-Required": "true"},
        )
    
    # Payment verified, make inference call
    try:
        response_text, tokens_used = await call_llm(
            body.prompt,
            body.model,
            body.max_tokens,
        )
        
        logger.info(f"Inference completed: {tokens_used} tokens, ${payment_amount/1_000_000:.6f} USDC")
        
        return InferenceResponse(
            response=response_text,
            model=body.model,
            payment_amount=payment_amount,
            tokens_used=tokens_used,
        )
        
    except Exception as e:
        logger.error(f"Inference failed: {e}")
        raise HTTPException(500, f"Inference failed: {e}")


@app.get("/pricing")
async def pricing():
    """Get current pricing for inference calls."""
    return {
        "price_per_call_usdc": PRICE_PER_CALL / 1_000_000,
        "price_per_call_raw": PRICE_PER_CALL,
        "network": "eip155:8453",
        "asset": "USDC",
        "recipient": RECIPIENT_ADDRESS,
    }


@app.get("/health")
async def health():
    return {"status": "ok", "x402_enabled": True}


# ============================================================================
# Run
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8402)
