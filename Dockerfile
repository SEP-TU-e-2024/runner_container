FROM python:3

# add basic dependencies
RUN apt-get update -y
RUN apt-get install -y sysstat time unzip build-essential
RUN pip install -U setuptools
RUN pip install -U wheel

WORKDIR /app

COPY start.sh start.sh
RUN chmod +x start.sh
COPY profiler.sh profiler.sh
RUN chmod +x profiler.sh

CMD ./start.sh
