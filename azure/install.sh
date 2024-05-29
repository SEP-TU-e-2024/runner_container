#!/bin/bash

# Add Docker apt repository
echo "-- pwd:"
pwd
echo "-- Adding Docker apt repository"
apt-get install -y ca-certificates curl
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
chmod a+r /etc/apt/keyrings/docker.asc

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null


# Update from the Docker apt repository, and install Docker
echo "-- Installing Docker"
apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin


# Install Python and dependencies
echo "-- Installing Python and dependencies"
apt-get install -y python3 python3-pip
pip install -r requirements.txt


# Copy judge runner to final program location
cp -r ./ /usr/local/bin/judge_runner/


# Create a systemd service file
echo "-- Creating service"
SERVICE_FILE=/etc/systemd/system/benchlab-judge-runner.service

echo "[Unit]
Description=BenchLab Judge Runner Service
After=network.target

[Service]
ExecStart=/usr/local/bin/judge_runner/mycode.py
WorkingDirectory=/usr/local/bin/judge_runner
Restart=always
User=nobody
Group=nogroup

[Install]
WantedBy=multi-user.target" | sudo tee $SERVICE_FILE


# Reload the systemd manager configuration
sudo systemctl daemon-reload

# Enable the service to start on boot
sudo systemctl enable benchlab-judge-runner.service

# Start the service immediately
sudo systemctl start benchlab-judge-runner.service

echo "-- All done"