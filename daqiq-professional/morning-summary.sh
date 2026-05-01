#!/bin/bash

echo "☀️  GOOD MORNING! OVERNIGHT DEVELOPMENT SUMMARY"
echo "=============================================="
echo ""
echo "📅 Date: $(date)"
echo ""

# Check agent completion
if pgrep -f "autonomous_roadmap_executor" > /dev/null; then
    echo "⚠️  Agent still running! (might need more time)"
else
    echo "✅ Agent completed!"
fi

echo ""
echo "📊 RESULTS:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Count all generated files
SCANNERS=$(find src/daqiq/scanners -name "*.py" ! -name "__init__.py" 2>/dev/null | wc -l)
TESTS=$(find tests -name "test_*.py" 2>/dev/null | wc -l)
DOCS=$(find docs -name "*.md" 2>/dev/null | wc -l)

echo "🔒 Security Scanners Generated: $SCANNERS"
echo "✅ Test Files Created: $TESTS"
echo "📚 Documentation Files: $DOCS"

# Git status
echo ""
echo "📝 Git Changes:"
NEW_FILES=$(git status --porcelain | grep "^??" | wc -l)
MODIFIED_FILES=$(git status --porcelain | grep "^ M" | wc -l)
echo "   • New files: $NEW_FILES"
echo "   • Modified files: $MODIFIED_FILES"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🚀 NEXT STEPS:"
echo ""
echo "1. Review generated code:"
echo "   ls -la src/daqiq/scanners/"
echo ""
echo "2. Run tests:"
echo "   pytest tests/ -v"
echo ""
echo "3. Commit changes:"
echo "   git add ."
echo "   git commit -m 'feat: AI-generated overnight development'"
echo "   git push"
echo ""
echo "4. Check detailed logs:"
echo "   cat logs/overnight/agent-*.log"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Show log summary
echo "📄 LOG SUMMARY:"
LATEST_LOG=$(ls -t logs/overnight/agent-*.log 2>/dev/null | head -1)
if [ -n "$LATEST_LOG" ]; then
    echo ""
    grep -i "generated\|completed\|error\|success" "$LATEST_LOG" | tail -20
fi

echo ""
echo "☕ Time for coffee while you review! 🎉"
echo ""
