#!/usr/bin/env python2
import click
from scapy.all import *
import re
from subprocess import call
from config import channelFrequencies, droneVendorMACs

detectedMACs = []

def changeToMonitorMode(interface):
	click.secho('-> Setting interface %s to monitor mode' % (interface), fg="bright_blue")
	call(['systemctl', 'stop', 'NetworkManager'])
	call(['ip', 'link', 'set', interface, 'down'])
	call(['iw', interface, 'set', 'monitor', 'control'])
	call(['ip', 'link', 'set', interface, 'up'])


def changeFrequency(interface, channel):
	freq = str(channelFrequencies[channel])
	click.secho('-> Setting interface %s to monitor on channel %s (%s MHz)' % (interface, channel, freq), fg="bright_green")
	call(['iw', 'dev', interface, 'set', 'freq', freq])
	del detectedMACs[:]


def changeToManagedMode(interface):
	click.secho('Setting interface %s to managed mode ' % (interface), fg="bright_green")
	call(['ip', 'link', 'set', interface, 'down'])
	call(['iw', interface, 'set', 'type', 'managed'])
	call(['ip', 'link', 'set', interface, 'up'])
	call(['systemctl', 'start', 'NetworkManager'])

def droneDetection(pkt):
	# create loop
	addressList = [pkt.addr1, pkt.addr2, pkt.addr3, pkt.addr4]
	isDroneMACAddress(addressList)

def isDroneMACAddress(addressList):
	for address in addressList:
		address = str(address)
		droneVendorMAC = droneVendorMACs.get(address[:8])
		if	re.match(r"([0-9a-fA-F]:?){12}", address) and droneVendorMAC != None and address not in detectedMACs:
			click.secho('Detected %s device with MAC address %s' % (droneVendorMAC, address) , fg="red", bold=True)
			detectedMACs.append(address)
