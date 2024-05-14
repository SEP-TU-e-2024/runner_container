FROM debian

# install basic dependencies at creation time
RUN apt-get update -y && apt-get install -y python3 python3-pip python3-venv time
#python3-psutil 

# create a user to run execute the code without privileges - no longer needed
# RUN useradd user

WORKDIR /

# add the starter scripts to the container
COPY starter_script.sh /scripts/starter_script.sh
# COPY timer.py /scripts/timer.py - no longer needed

# make the bash script executable
RUN chmod +x /scripts/starter_script.sh

# WORKDIR /runtime

# run the script - main command
CMD ["/scripts/starter_script.sh"]