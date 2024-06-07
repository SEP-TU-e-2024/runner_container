FROM python:3

# add basic dependencies
RUN apt-get update
RUN apt-get install -y sysstat
# this is for mpstat

#RUN apt-get update -y && apt-get install -y python3 python3-pip python3-venv 

WORKDIR /

COPY start.sh start.sh
RUN chmod +x start.sh
COPY profiler.sh profiler.sh
RUN chmod +x profiler.sh

CMD ./start.sh

# CHANGE THIS DOCKERFILE, THIS IS JUST FOR TESTING