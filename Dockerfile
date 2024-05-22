FROM python:3
#FROM debian

# install basic dependencies at creation time
#RUN apt-get update -y && apt-get install -y python3 python3-pip python3-venv 

WORKDIR /

COPY start.sh start.sh
RUN chmod +x start.sh

CMD ./start.sh