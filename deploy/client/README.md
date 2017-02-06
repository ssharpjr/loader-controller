# Raspberry Pi Client Setup


## Raspberry Pi Initial Configuration
##### Raspi-Config
Using a Raspberry Pi3 running Raspian Jessie Lite 01-11-2017
Run
```shell
sudo raspi-config
```

Perform the following steps:
1. Expand Filesystem
2. Change User Password
3. International Options
  a. Change locale to en_US.UTF-8 UTF-8.
  b. Change Timezone to US/Eastern.
  c. Change Keyboard Layout to 104-Key US Generic
4. Advanced Options
  a. Set Hostname
  b. Enable SSH
  c. Enable I2C
5. Reboot

##### Setup Wireless Networking
Edit wpa_supplicant.conf.
```shell
sudo nano /etc/wpa_supplicant_wpa_supplicant.conf
```

Add the following to the end of this file:
```shell
network={
ssid="TPINET"
psk="SUPERSECRETKEY"
}
```
Reboot


## Software Installation
##### Install the necessary packages
```shell
sudo apt-get update
sudo apt-get install -y vim build-essential python3-dev python3-smbus \
python3-pip git rpi-update python3-rpi.gpio i2c-tools
```

##### Setup VIM
Setup Dot File
```shell
git clone https://github.com/ssharpjr/dotfiles.git
cd dotfiles
cp vimrc.rpi /home/pi/.vimrc
./install_vundle.sh
```

##### Clone Repositories
Clone the Loader Controller Repo
```shell
git clone https://github.com/ssharpjr/loader-controller.git
```

##### Install pip software
```shell
cd loader-controller
sudo pip3 install -r requirements.txt
```

##### Clone Hardware Repositories
```shell
cd
git clone https://github.com/adafruit/Adafruit_Python_GPIO
cd Adafruit_Python_GPIO && sudo python3 setup.py install
git clone https://github.com/adafruit/Adafruit_Python_CharLCD
cd Adafruit_Python_CharLCD && sudo python3 setup.py install
```

##### Create Maintenance User Account
```shell
sudo adduser USERNAME
sudo usermod -G adm,dialout,cdrom,sudo,audio,video,plugdev,games,users,input,\
     netdev,spi,i2c,gpio -a USERNAME
```

##### Setup Autologin
Create a systemd startup file
```shell
sudo vi /etc/systemd/system/getty@tty1.service.d/autologin.conf
```

Enter the following:
```shell
[Service]
ExecStart=
ExecStart=-/sbin/agetty --autologin pi --noclear %I 38400 linux
```

Start the service
```shell
sudo systemctl enable getty@tty1.service
```

##### Setup AutoStart Script
Edit the .bashrc for pi
```shell
vi /home/pi/.bashrc
```

Enter the following at the end of the file:
```shell
# Run Loader Controller
cd loader-controller
python3 loader-controller.py
```

