FROM debian

# install basic dependencies at creation time
RUN apt-get update
RUN apt-get upgrade
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get install -y python3-venv

# add the starter script to the container
COPY starter_script.sh /usr/local/bin/starter_script.sh

# make the script executable
RUN chmod +x /usr/local/bin/starter_script.sh

# run the script - main command
CMD ["/usr/local/bin/starter_script.sh"]