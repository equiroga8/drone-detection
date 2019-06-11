from subprocess import call
from termcolor import colored
import sys

# systemctl stop NetworkManager
# ip link set wlp2s0 down
# iw wlp2s0 set monitor control
# ip link set wlp2s0 up
# iw dev wlp2s0 set freq
# ...
# ip link set wlp2s0 down
# iw wlp2s0 set type managed
# ip link set wlp2s0 up
# systemctl start NetworkManager

print colored("-> Printing message", 'green')
call("echo \"hello how are you\"", shell = True)

