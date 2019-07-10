#!/usr/bin/env python2
import click
from scapy.all import *
import re
from subprocess import call
from constants import CHANNEL_FREQUENCIES, DRONE_VENDOR_MACS

detected_MACs = []

def change_to_monitor_mode(interface):
	click.secho('-> Setting interface %s to monitor mode' % (interface), fg="bright_blue")
	call(['systemctl', 'stop', 'NetworkManager'])
	call(['ip', 'link', 'set', interface, 'down'])
	call(['iw', interface, 'set', 'monitor', 'control'])
	call(['ip', 'link', 'set', interface, 'up'])


def change_frequency(interface, channel):
	freq = str(CHANNEL_FREQUENCIES[channel])
	click.secho('-> Setting interface %s to monitor on channel %s (%s MHz)' % (interface, channel, freq), fg="bright_green")
	call(['iw', 'dev', interface, 'set', 'freq', freq])
	del detected_MACs[:]


def change_to_managed_mode(interface):
	click.secho('Setting interface %s to managed mode ' % (interface), fg="bright_green")
	call(['ip', 'link', 'set', interface, 'down'])
	call(['iw', interface, 'set', 'type', 'managed'])
	call(['ip', 'link', 'set', interface, 'up'])
	call(['systemctl', 'start', 'NetworkManager'])

def drone_detection(packet):
	try:
		address_list = [packet.addr1, packet.addr2, packet.addr3, packet.addr4]
		is_drone_MAC_address(address_list)
	except AttributeError:
		pass

def is_drone_MAC_address(address_list):
	for address in address_list:
		address = str(address)
		drone_vendor_MAC = DRONE_VENDOR_MACS.get(address[:8])
		if	re.match(r"([0-9a-fA-F]:?){12}", address) and drone_vendor_MAC != None and address not in detected_MACs:
			click.secho('Detected %s device with MAC address %s' % (drone_vendor_MAC, address) , fg="red", bold=True)
			detected_MACs.append(address)
