FROM debian

# install basic dependencies at creation time
RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get install -y python3-venv
RUN apt-get install -y python3-psutil
RUN apt-get install -y time
# RUN apt-get install -y python3-time

RUN useradd user

WORKDIR /

# add the starter scripts to the container
COPY starter_script.sh /scripts/starter_script.sh
COPY timer.py /scripts/timer.py

# make the bash script executable
RUN chmod +x /scripts/starter_script.sh

# WORKDIR /runtime

# run the script - main command
CMD ["/scripts/starter_script.sh"]