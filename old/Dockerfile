FROM debian

# install basic dependencies at creation time
RUN apt-get update -y && apt-get install -y python3 python3-pip python3-venv unzip
#python3-psutil 

# create a user to run execute the code without privileges - no longer needed
# RUN useradd user

WORKDIR /

# add user code to container
COPY target.zip /target.zip

# unzip user code and put it in /
RUN unzip target.zip
RUN mv target/* .
RUN rm target

# Make run.sh executable
RUN chmod +x run.sh


# WORKDIR /runtime

# run the script - main command
CMD ["run.sh"]