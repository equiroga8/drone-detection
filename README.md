# Dronitor

Dronitor is a command line tool capable of detecting drones (or any other device) by checking the MAC address of the devices communicating on a specific/any WiFi channel.

## Prerequisites

Dronitor was tested on Ubuntu 18.04  and for it to work it needs a wireless network card that supports monitor mode. To find out your computer's wireless interface name type in the terminal:

```
iw dev
```

This lists your computer's wireless interfaces. Remember the name of the wireless interface because it will be needed later. It will usually have a name similar to `wlp2s0` or `wlan0`.

To find out if the your wireless interface supports monitor mode type:

```
iw list | grep monitor
```

If monitor appears in the output that means that the interface can be put in monitor mode and that you can use dronitor on your computer. 

This program uses python 2.7 and pip. Make sure you have both installed (you can check the version by typing `$ python -V`) in the terminal. If you don't, you can install them using the terminal.
```
sudo apt update
sudo apt upgrade
sudo apt install python2.7 python-pip
```
## Installation

This program uses python 2.7 and various libraries such as [Click](https://click.palletsprojects.com/en/7.x/), to create a command line interface and [Scapy](https://scapy.readthedocs.io/en/latest/introduction.html), to sniff and dissect network packets. To install dronitor follow these steps:

Clone the repository.
```
git clone https://github.com/equiroga8/drone-detection.git
cd drone-detection
```
Install all the necessary libraries and modules.

```
pip install -r requirements.txt
```

You can now start using dronitor.


## Usage

Dronitor detects devices by scaning all the packets in a channel for MAC addresses in a certain range. It uses the Organizational Unique Identifier (OUI) which is the first 24 bits of a MAC address. This indicates the specific vendor for that device. 

<img src="https://aacable.files.wordpress.com/2018/02/mac-address.gif?w=435&h=196" align="right">

The OIUs for which dronitor creates an alert can be modified by editing `droneVendorMACs` in `constants.py` and adding a key value pair. For example one of the OIUs assigned to Samsung is `04:d6:aa`. You can find more OUIs [here](https://mac-oui.com/). 

This tool has 3 different commands. We will explain them one by one. 

#### Static
With this command you can scan for drones on a specific WiFi channel. 
```
sudo ./dronitor static wlp2s0 -c 1
```
First it changes the wireless network card to monitor mode and scans all the WiFi packets on channel 1. If it finds a MAC address with an OUI that is on the list an alert will appear. In this command `wlp2s0` is the name of the wireless interface and `-c` indicates the [channel](https://www.electronics-notes.com/articles/connectivity/wifi-ieee-802-11/channels-frequencies-bands-bandwidth.php) to listen on. You can also use `--channel` for more verbosity. To exit press `ctrl-c`.

#### Hop
With this command you can scan for drones on all the WiFi channels.
```
sudo ./dronitor hop wlp2s0 -t 0.5
```
First it changes the wireless network card to monitor mode and then scans all the WiFi packets. It changes channel every 0.5 seconds and loops constantly through all the WiFi channels. If it finds a MAC address with an OUI that is on the list an alert will appear. In this command `wlp2s0` is the name of the wireless interface that will be used and `-t` or `--time` is the time to wait before changing to the next channel. To exit press `ctrl-c` for a few seconds.

#### Managed

With this command you can change your wireless interface back to managed mode. 
```
sudo ./dronitor managed wlp2s0
```
Where `wlp2s0` is the name of the wireless interface that will be changed to managed mode. Use this command when you've finished using dronitor.