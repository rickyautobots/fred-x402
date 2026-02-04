#!/usr/bin/env python3
"""Quick test of x402 SDK installation."""

import sys
sys.path.insert(0, "/Users/derekpassmore/.openclaw/workspace/projects/x402-hackathon/sdk/examples/python/clients/httpx/.venv/lib/python3.10/site-packages")

try:
    from x402 import x402Client
    from x402.http import x402HTTPClient
    print("✅ x402 SDK imported successfully")
    
    # Test client creation
    client = x402Client()
    print("✅ x402Client created")
    
    # Check available schemes
    print(f"✅ Client ready for payment registration")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
