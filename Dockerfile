FROM debian

# add basic dependencies
RUN apt-get update -y && apt-get install -y python3 python3-pip python3-venv
RUN apt-get install unzip 

WORKDIR /app

COPY start.sh start.sh
RUN chmod +x start.sh
COPY profiler.sh profiler.sh
RUN chmod +x profiler.sh

CMD ./start.sh