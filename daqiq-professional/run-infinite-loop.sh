#!/bin/bash

echo "🔁 INFINITE AUTONOMOUS DEVELOPMENT LOOP"
echo "======================================="
echo ""

cd ~/daqiq-dev/daqiq-professional
export PYTHONPATH="$(pwd)/src:$PYTHONPATH"

ITERATION=1

while true; do
    echo ""
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║  🔄 ITERATION #$ITERATION - $(date '+%H:%M:%S')                              ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo ""
    
    # Run the autonomous executor
    python3 scripts/autonomous_roadmap_executor.py \
        --batch-size 5 \
        --max-iterations 20 \
        2>&1 | tee -a logs/overnight/infinite-loop-$(date +%Y%m%d).log
    
    # Count what we have
    SCANNER_COUNT=$(find src/daqiq/scanners autonomous_development -name "*.py" ! -name "__init__.py" 2>/dev/null | wc -l)
    
    echo ""
    echo "📊 Current Status:"
    echo "   Iteration: $ITERATION"
    echo "   Scanners Generated: $SCANNER_COUNT"
    echo "   Time: $(date)"
    echo ""
    
    # Stop after we have enough (60+ scanners)
    if [ $SCANNER_COUNT -ge 60 ]; then
        echo "🎉 TARGET REACHED! $SCANNER_COUNT scanners generated!"
        break
    fi
    
    ITERATION=$((ITERATION + 1))
    
    echo "⏳ Waiting 30 seconds before next iteration..."
    sleep 30
done

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  ✅ AUTONOMOUS DEVELOPMENT COMPLETE!                        ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "📊 Final Stats:"
echo "   Total Scanners: $(find src/daqiq/scanners autonomous_development -name "*.py" ! -name "__init__.py" 2>/dev/null | wc -l)"
echo "   Iterations: $ITERATION"
echo "   Finished: $(date)"
echo ""
