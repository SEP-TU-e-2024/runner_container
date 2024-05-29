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

# Make 
ENTRY=mycode.py
chmod +x /usr/local/bin/judge_runner/$ENTRY


# Define service
echo "-- Creating service"
SERVICE_FILE=/etc/systemd/system/benchlab-judge-runner.service

echo "[Unit]
Description=BenchLab Judge Runner Service
After=network.target

[Service]
ExecStart=/usr/local/bin/judge_runner/$ENTRY
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

# Health check: wait until the service has been running stably for a few seconds
HEALTHCHECK_INTERVAL=1  # seconds
HEALTHCHECK_DURATION=5 # seconds
HEALTHCHECK_PASSED=false

# doesnt work yet, if crash and restarted immediately, it likely doesnt catch the crash

for ((i=1; i<=HEALTHCHECK_DURATION; i+=HEALTHCHECK_INTERVAL)); do
    sleep $HEALTHCHECK_INTERVAL
    SERVICE_STATUS=$(systemctl is-active benchlab-judge-runner.service)
    if [[ "$SERVICE_STATUS" == "active" ]]; then
        echo "Service is running... ($i seconds)"
        if [[ $i -ge $HEALTHCHECK_DURATION ]]; then
            HEALTHCHECK_PASSED=true
            break
        fi
    else
        echo "Service is not running properly. Status: $SERVICE_STATUS"
        break
    fi
done

if $HEALTHCHECK_PASSED; then
    echo "Health check passed: The BenchLab Judge Runner service is running stably."
else
    echo "Health check failed: The BenchLab Judge Runner service did not reach stable running state."
    exit 1
fi

echo "-- All done"
