#!/bin/bash

echo "📊 AGENT PROGRESS REPORT"
echo "========================"
echo ""

# Check if agent is running
if [ -f /tmp/daqiq-agent.pid ]; then
    PID=$(cat /tmp/daqiq-agent.pid)
    if ps -p $PID > /dev/null; then
        echo "✅ Agent Status: RUNNING (PID: $PID)"
        UPTIME=$(ps -o etime= -p $PID)
        echo "⏱️  Running for: $UPTIME"
    else
        echo "❌ Agent Status: STOPPED"
    fi
else
    echo "❌ Agent Status: NOT STARTED"
fi

echo ""
echo "📈 Progress:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Count generated scanners
SCANNER_COUNT=$(find src/daqiq/scanners -name "*.py" ! -name "__init__.py" 2>/dev/null | wc -l)
echo "🔒 Security Scanners: $SCANNER_COUNT"

# Count test files
TEST_COUNT=$(find tests -name "test_*.py" 2>/dev/null | wc -l)
echo "✅ Test Files: $TEST_COUNT"

# Check latest log
LATEST_LOG=$(ls -t logs/overnight/agent-*.log 2>/dev/null | head -1)
if [ -n "$LATEST_LOG" ]; then
    echo ""
    echo "📄 Latest Log: $LATEST_LOG"
    echo ""
    echo "Last 10 entries:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    tail -10 "$LATEST_LOG"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🔄 To see live updates:"
echo "   tail -f logs/overnight/agent-*.log"
echo ""
