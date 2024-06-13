docker context use default
docker build --no-cache -t runnercontainer .
echo "y" | docker system prune