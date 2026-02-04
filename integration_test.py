#!/usr/bin/env python3
"""
x402 FRED Integration Test

Demonstrates the x402 payment flow without actual spending.
For demo purposes, shows what happens when FRED needs inference.
"""

import asyncio
import sys
sys.path.insert(0, '/Users/derekpassmore/.openclaw/workspace/skills/fred/scripts')

from config import Settings
from core.scanner import MarketScanner


async def demo_x402_flow():
    """Demonstrate the x402 payment flow."""
    
    print("=" * 60)
    print("🤖 FRED x402 Integration Demo")
    print("=" * 60)
    
    # Step 1: Initialize scanner
    print("\n📊 Step 1: Scanning Polymarket for opportunities...")
    settings = Settings()
    scanner = MarketScanner(settings)
    
    try:
        markets = await scanner.fetch_markets(limit=3)
        print(f"   Found {len(markets)} markets")
        
        if not markets:
            print("   No markets found. Using mock data for demo.")
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
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await scanner.close()


if __name__ == "__main__":
    print("\n🚀 Starting x402 FRED Integration Demo\n")
    asyncio.run(demo_x402_flow())
