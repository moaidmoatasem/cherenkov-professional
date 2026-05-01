#!/bin/bash

cd ~/daqiq-dev/daqiq-professional

# Activate venv
source .venv/bin/activate

# Set Python path
export PYTHONPATH="$(pwd)/src:$PYTHONPATH"

# Create logs
mkdir -p logs/overnight

# Start Ollama if needed
pgrep -x ollama > /dev/null || (ollama serve &)
sleep 3

echo "🚀 Starting agents..."
echo "📝 Log: logs/overnight/agent-$(date +%Y%m%d-%H%M%S).log"

# Run with proper path
cd ~/daqiq-dev/daqiq-professional && \
PYTHONPATH="$(pwd)/src:$PYTHONPATH" \
nohup python scripts/autonomous_roadmap_executor.py \
    --batch-size 3 \
    --max-iterations 30 \
    > logs/overnight/agent-$(date +%Y%m%d-%H%M%S).log 2>&1 &

echo "✅ PID: $!"
echo $! > /tmp/daqiq-agent.pid
