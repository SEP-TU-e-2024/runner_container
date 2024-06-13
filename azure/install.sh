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
apt-get install -y software-properties-common wget
add-apt-repository -y ppa:deadsnakes/ppa
apt-get update
apt-get install -y python3.12 python3.12-venv
wget https://bootstrap.pypa.io/get-pip.py -O get-pip.py
python3.12 get-pip.py

python3.12 -m pip install -r requirements.txt


# Copy judge runner to final program location
cp -r ./ /usr/local/bin/judge_runner/

ENTRYPOINT=runner.py
chmod +x /usr/local/bin/judge_runner/$ENTRYPOINT

cd /usr/local/bin/judge_runner/
docker build -t runnercontainer .

# Define service
echo "-- Creating service"
SERVICE_FILE=/etc/systemd/system/benchlab-judge-runner.service

echo "[Unit]
Description=BenchLab Judge Runner Service
After=network.target

[Service]
ExecStart=/usr/local/bin/judge_runner/$ENTRYPOINT
WorkingDirectory=/usr/local/bin/judge_runner
Restart=always
User=root
Group=root

[Install]
WantedBy=multi-user.target" | tee $SERVICE_FILE


# Load, enable and start service
echo "-- Starting service"
systemctl daemon-reload
systemctl enable benchlab-judge-runner.service
systemctl start benchlab-judge-runner.service


# Wait for 3 seconds to see if service stable
echo "-- Checking service health"
sleep 3

RESTART_COUNT=$(systemctl show -p NRestarts benchlab-judge-runner.service | cut -d'=' -f2)
if [[ "$RESTART_COUNT" -gt 0 ]]; then
    echo "-- Service has restarted $RESTART_COUNT times. Health check failed."
    exit 1
fi

SERVICE_STATUS=$(systemctl is-active benchlab-judge-runner.service)
if [[ "$SERVICE_STATUS" != "active" ]]; then
    echo "-- Service is not running properly. Status: $SERVICE_STATUS"
    exit 1
fi

echo "-- Health check passed"

echo "-- All done"
