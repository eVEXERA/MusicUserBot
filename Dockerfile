Telegram @Itz_Your_4Bhi
Copyright ©️ 2025



FROM python:3.9-slim-buster

# Updating Packages
RUN apt update && apt upgrade -y
RUN apt install git curl python3-pip ffmpeg -y

# Copying Requirements
COPY requirements.txt /requirements.txt

# Installing Requirements
RUN cd /
RUN pip3 install --upgrade pip
RUN pip3 install -U -r requirements.txt

# Setting up working directory
RUN mkdir /MusicUserBot
WORKDIR /MusicUserBot

# Preparing for the Startup
COPY abhi.sh /abhi.sh
RUN chmod +x /abhi.sh

# Running Music User Bot
CMD ["/bin/bash", "/abhi.sh"]
