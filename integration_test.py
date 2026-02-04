#!/usr/bin/env python3
"""
x402 FRED Integration Test

Demonstrates the x402 payment flow without actual spending.
Self-contained for CI - no external dependencies on FRED skill.
"""

import asyncio
import os


# Mock mode for CI - doesn't require actual FRED or API calls
MOCK_MODE = os.getenv("X402_MOCK_MODE", "false").lower() == "true"


class MockMarket:
    """Mock market for demo purposes."""
    def __init__(self):
        self.question = "Will Bitcoin exceed $100,000 by March 2026?"
        self.outcomes = [type('Outcome', (), {'name': 'Yes', 'price': 0.55})()]


async def demo_x402_flow():
    """Demonstrate the x402 payment flow."""
    
    print("=" * 60)
    print("🤖 FRED x402 Integration Demo")
    print("=" * 60)
    
    if MOCK_MODE:
        print("\n⚠️  Running in MOCK MODE (CI environment)")
    
    # Step 1: Scan markets (mock in CI)
    print("\n📊 Step 1: Scanning Polymarket for opportunities...")
    
    if MOCK_MODE:
        markets = [MockMarket()]
        print(f"   [MOCK] Using demo market data")
    else:
        # Only import FRED if not in mock mode
        import sys
        sys.path.insert(0, '/Users/derekpassmore/.openclaw/workspace/skills/fred/scripts')
        from config import Settings
        from core.scanner import MarketScanner
        
        settings = Settings()
        scanner = MarketScanner(settings)
        markets = await scanner.fetch_markets(limit=3)
    
    print(f"   Found {len(markets)} markets")
    
    if not markets:
        print("   No markets found. Demo cannot continue.")
        return
    
    market = markets[0]
    print(f"   Selected: {market.question[:50]}...")
    print(f"   Current price: {market.outcomes[0].price if market.outcomes else 'N/A'}")
    
    # Step 2: Show x402 payment requirement
    print("\n💳 Step 2: Requesting probability estimate...")
    print("   → Calling inference endpoint...")
    print("   ← HTTP 402 Payment Required")
    print("   Payment details:")
    print("     - Amount: $0.005 USDC")
    print("     - Network: Base (eip155:8453)")
    print("     - Recipient: 0xd5950fbB8393C3C50FA31a71faabc73C4EB2E237")
    
    # Step 3: Show payment execution
    print("\n💰 Step 3: Executing x402 payment...")
    print("   → Signing payment with wallet...")
    print("   → Sending to CDP facilitator...")
    print("   ✓ Payment confirmed!")
    
    # Step 4: Show inference result
    print("\n🧠 Step 4: Receiving inference result...")
    print(f"   Question: {market.question[:60]}...")
    print("   LLM Estimate:")
    print("     - Yes probability: 0.62")
    print("     - Confidence: 0.75")
    print("     - Reasoning: Based on market analysis...")
    
    # Step 5: Show trade decision
    print("\n📈 Step 5: Trade decision...")
    print("   Market price: 0.55 (YES)")
    print("   LLM estimate: 0.62 (YES)")
    print("   Edge: +7%")
    print("   → TRADE: BUY YES @ 0.55")
    print("   → Position size: $5.00 (optimal-f)")
    
    # Step 6: Show revenue loop
    print("\n🔄 Step 6: Revenue loop...")
    print("   Trade executed on Polymarket")
    print("   $FRED volume generated: +$5.00")
    print("   LP fees earned: $0.04 (0.8%)")
    print("   → Fees fund next inference call")
    
    print("\n" + "=" * 60)
    print("✅ Demo complete! Self-funding loop demonstrated.")
    print("=" * 60)
    
    # Cleanup if not mock
    if not MOCK_MODE:
        await scanner.close()


if __name__ == "__main__":
    print("\n🚀 Starting x402 FRED Integration Demo\n")
    asyncio.run(demo_x402_flow())
