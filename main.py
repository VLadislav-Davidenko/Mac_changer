#!/usr/bin/env python

import subprocess
import optparse
import re


def get_arguments():
    """ Here we are creating parser Object and add some option to input interface
    and MAC address which we want to change to. After User input we get
    (options and arguments) such as (eth0 and interface) arguments 'dest'
    that we wrote in function add_option"""
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options, arguments) = parser.parse_args()
    # Here we check if user do not forget to input a variables interface or new_mac
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info")
    elif not options.new_mac:
        parser.error("[-] Please specify a new mac address, use --help for more info")
    else:
        return options


def change_mac(interface, new_mac):
    """Here we use library subprocess to use terminal inside or code via function call
    Everything is written in the list to avoid hijacking in our terminal"""
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface):
    """This function get the output of ifconfig command and via library of
    Regular expression (re) we catch our MAC address"""
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
    # Checking if we have at least on MAC address or take the first one in a group of addresses
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("Could not read MAC address.")


# Calling our functions
options = get_arguments()
current_mac = get_current_mac(options.interface)
print("Current MAC = " + str(current_mac))

change_mac(options.interface, options.new_mac)
current_mac = get_current_mac(options.interface)

# Checking if the changes happened
if current_mac == options.new_mac:
    print("[+] MAC address was successfully changed to " + current_mac)
else:
    print("[-] MAC address did not get changed")
