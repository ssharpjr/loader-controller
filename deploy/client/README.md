# Raspberry Pi Client Setup

## Software Installation
##### Install the necessary packages
```shell
sudo apt-get update
sudo apt-get install -y build-essential python3-dev python3-smbus \
python3-pip git rpi-update python3-rpi.gpio i2c-tools
```

##### Install pip software
```shell

```

## Configuration
##### Load Kernel Modules
```shell
sudo vi /etc/modules
...
```

##### Add Modules to Config.txt
```shell
sudo vi /boot/config.txt
...
```

##### Create Maintenance User Account
```shell
...
```

## Setup Read Only Filesystem
...
