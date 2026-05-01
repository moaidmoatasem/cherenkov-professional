#!/bin/bash

echo "🔶 Oracle Cloud FREE Tier Setup"
echo "================================"
echo ""
echo "✅ FREE FOREVER Resources:"
echo "   • 2 AMD VMs (1/8 OCPU, 1GB RAM each)"
echo "   • 4 ARM VMs (24GB RAM total!)"
echo "   • 200GB Block Storage"
echo "   • 10GB Object Storage"
echo "   • Load Balancer"
echo ""
echo "📝 Setup Steps:"
echo ""
echo "1. Sign up: https://cloud.oracle.com/free"
echo "2. Create VM Instance:"
echo "   - Shape: VM.Standard.A1.Flex (ARM)"
echo "   - OCPUs: 4 (max free)"
echo "   - RAM: 24GB (max free)"
echo "   - OS: Ubuntu 22.04"
echo ""
echo "3. SSH into VM and run:"
echo ""
cat << 'SETUP'
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# Install Ollama
curl https://ollama.ai/install.sh | sh
ollama serve &
ollama pull qwen2.5:3b

# Clone & Deploy DAQIQ
git clone git@github.com:moaidmoatasem/daqiq-professional.git
cd daqiq-professional
docker compose -f deploy/docker-compose.yml up -d

# Setup systemd service
sudo tee /etc/systemd/system/daqiq.service << SERVICE
[Unit]
Description=DAQIQ Security Scanner
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=/home/$USER/daqiq-professional
ExecStart=/usr/bin/docker compose -f deploy/docker-compose.yml up
Restart=always

[Install]
WantedBy=multi-user.target
SERVICE

sudo systemctl enable daqiq
sudo systemctl start daqiq

echo "✅ DAQIQ deployed on Oracle Cloud!"
echo "🌐 Access: http://$(curl -s ifconfig.me):5000"
SETUP
