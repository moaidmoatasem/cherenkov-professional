#!/bin/bash

echo "🌙 OVERNIGHT AUTONOMOUS DEVELOPMENT"
echo "===================================="
echo ""
echo "⏰ Starting at: $(date)"
echo "🎯 Estimated completion: 8-12 hours"
echo ""

# Set Python path
export PYTHONPATH="$(pwd)/src:$PYTHONPATH"

# Ensure Ollama is running
if ! pgrep -x "ollama" > /dev/null; then
    echo "🧠 Starting Ollama..."
    ollama serve > /tmp/ollama.log 2>&1 &
    sleep 5
fi

# Ensure model is available
if ! ollama list | grep -q "qwen2.5:3b"; then
    echo "📥 Pulling AI model..."
    ollama pull qwen2.5:3b
fi

echo "✅ Ollama ready!"
echo ""

# Create logs directory
mkdir -p logs/overnight

# Activate virtual environment
source .venv/bin/activate

# Start autonomous development with Python path set
echo "🤖 Starting autonomous agents..."
echo "   • Mode: Continuous"
echo "   • Batch size: 5 scanners at a time"
echo "   • Max iterations: 50 (all tasks)"
echo "   • Python Path: $PYTHONPATH"
echo "   • Logging: logs/overnight/agent-$(date +%Y%m%d-%H%M%S).log"
echo ""

nohup python scripts/autonomous_roadmap_executor.py \
    --batch-size 5 \
    --max-iterations 50 \
    --continuous \
    > logs/overnight/agent-$(date +%Y%m%d-%H%M%S).log 2>&1 &

AGENT_PID=$!
echo "✅ Agent started! PID: $AGENT_PID"
echo ""

# Save PID for monitoring
echo $AGENT_PID > /tmp/daqiq-agent.pid

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🎯 TASKS QUEUED:"
echo "   • 30+ Security Scanners"
echo "   • API Security Tools"
echo "   • Compliance Checkers"
echo "   • Documentation Generation"
echo "   • Code Optimization"
echo "   • Test Suite Expansion"
echo ""
echo "📊 MONITORING:"
echo "   • Watch logs: tail -f logs/overnight/agent-*.log"
echo "   • Check status: ps -p $AGENT_PID"
echo "   • View progress: cat logs/overnight/agent-*.log | grep 'Generated'"
echo ""
echo "🛑 TO STOP:"
echo "   • Kill agent: kill $AGENT_PID"
echo "   • Or run: pkill -f autonomous_roadmap_executor"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "😴 Go to sleep! Your agents are working..."
echo ""
