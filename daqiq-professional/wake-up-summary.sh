#!/bin/bash

echo "☀️  صباح الخير MOAID! MORNING SUMMARY"
echo "====================================="
echo ""
echo "📅 Time: $(date)"
echo ""

# Check if still running
AGENT_PID=363901

if ps -p $AGENT_PID > /dev/null 2>&1; then
    echo "⚠️  Agent STILL RUNNING (needs more time)"
    RUNTIME=$(ps -p $AGENT_PID -o etime= 2>/dev/null | xargs)
    echo "   Running for: $RUNTIME"
else
    echo "✅ Agent COMPLETED!"
fi

echo ""
echo "📊 RESULTS:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

SCANNERS=$(find src/daqiq/scanners autonomous_development -name "*.py" ! -name "__init__.py" 2>/dev/null | wc -l)
TESTS=$(find tests -name "test_*.py" 2>/dev/null | wc -l)

echo "🔒 Total Security Scanners: $SCANNERS"
echo "✅ Total Test Files: $TESTS"
echo ""

echo "📝 Latest generated scanners:"
find src/daqiq/scanners autonomous_development -name "*.py" ! -name "__init__.py" -type f 2>/dev/null | \
    xargs ls -lt 2>/dev/null | head -10 | awk '{print "   " $9}'

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🚀 NEXT STEPS:"
echo "   1. Review code: ls -la src/daqiq/scanners/"
echo "   2. Run tests: pytest tests/ -v"
echo "   3. Check log: cat logs/overnight/extended-20260501-064147.log | less"
echo "   4. Commit: git add . && git commit -m 'feat: AI overnight development' && git push"
echo ""
