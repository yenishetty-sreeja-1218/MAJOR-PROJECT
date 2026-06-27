#!/bin/bash
# setup.sh - Install Dask + Ray and verify installation

echo "=== Creating Virtual Environment ==="
python3 -m venv venv
source venv/bin/activate

echo ""
echo "=== Installing Dependencies from requirements.txt ==="
pip install -r requirements.txt

echo ""
echo "=== Running Tests ==="
python3 ../tests/test_environment.py | tee test_results.log

echo ""
if grep -q "All tests passed" test_results.log; then
    echo "=== SUCCESS: All tests passed. Results saved to test_results.log ==="
else
    echo "=== FAILED: Check test_results.log for details ==="
fi
