FROM python:3

# add basic dependencies
RUN apt update -y
RUN apt install unzip

WORKDIR /

COPY start.sh start.sh
RUN chmod +x start.sh
COPY profiler.sh profiler.sh
RUN chmod +x profiler.sh

CMD ./start.sh