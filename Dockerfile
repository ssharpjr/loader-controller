FROM resin/%%RESIN_MACHINE_NAME%%-python:3.5

# Install Packages
RUN apt-get update && apt-get install -y build-essential python3-dev \
    python3-smbus python3-pip git rpi-update python3-rpi.gpio i2c-tools

# Get and Install Repositories
RUN mkdir src
RUN cd src
RUN git clone https://github.com/adafruit/Adafruit_Python_CharLCD
RUN git clone https://github.com/adafruit/Adafruit_Python_GPIO
RUN cd Adafruit_Python_CharLCD
RUN python3 setup.py install
RUN cd ../Adafruit_Python_GPIO
RUN python3 setup.py install

# Activate Modules
RUN echo 'i2c-bcm2708 >> /etc/modules'
RUN echo 'i2c-dev >> /etc/modules'

# Set working directory
WORKDIR = /home/pi/loader-controller

# Copy and Install Requirements
COPY ./requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

# Copy all files in our root the working directory
COPY . ./

# Switch on systemd in container
ENV INITSYSTEM on

# Start the application on startup
CMD ["python3","loader-controller.py"]

