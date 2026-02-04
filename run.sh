#!/bin/bash
# x402 FRED Quick Start
# Usage: ./run.sh [demo|server|test]

set -e

cd "$(dirname "$0")"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🤖 FRED x402 Integration${NC}"
echo "========================="

# Check for venv
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
else
    source .venv/bin/activate
fi

case "${1:-demo}" in
    demo)
        echo -e "\n${GREEN}Running x402 demo...${NC}\n"
        python test_x402.py
        ;;
    server)
        echo -e "\n${GREEN}Starting x402 inference server on :8402...${NC}\n"
        cd fred-integration
        uvicorn x402_inference_server:app --host 0.0.0.0 --port 8402 --reload
        ;;
    test)
        echo -e "\n${GREEN}Running integration test...${NC}\n"
        python integration_test.py
        ;;
    *)
        echo "Usage: ./run.sh [demo|server|test]"
        echo "  demo   - Run the x402 payment demo"
        echo "  server - Start the inference server"
        echo "  test   - Run full integration test"
        exit 1
        ;;
esac
