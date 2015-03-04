__author__ = 'Leonardo Rafaeli'
import pickle
import os
from argparse import ArgumentParser
import re

class OctetTree:
    def __init__(self, octet, children):
        self.octet = octet
        self.children = children

class IpInfo:
    def __init__(self, ipAddress, note):
        self.ipAddress = ipAddress
        self.note = note

    def setIpAddress(self, ipAddress):
        self.ipAddress = ipAddress

    def getIpAddress(self):
        return self.ipAddress

    def setNote(self, note):
        self.note = note

    def getNote(self):
        return self.note

    def describe(self):
        print(self.to_str())

    def to_str(self):
        return "IP: " + self.ipAddress + ", Note: " + self.note

def print_infos(infos):
    for info in infos:
        info.describe()

def main():
    parser = ArgumentParser(description="Insert and Lookup for IP addresses")
    parser.add_argument("-l", "--list", help="List all available IPs in the database", action="store_true")
    parser.add_argument("-a", "--add", help="Add a new IP to the database", nargs="+", metavar=("IP", "NOTES"))
    parser.add_argument("-sc", "--search-note", help="Search an IP by note", metavar="NOTES")
    parser.add_argument("-si", "--search-ip", help="Search IP by address", metavar="IP")
    parser.add_argument("-sn", "--search-network", help="Search IP by network", metavar="IP")

    args = parser.parse_args(["-a", "192.1.255.1/12"])

    if args.list:
        list_infos()
    if args.add:
        #save_info(args.add[0], args.add[1])
        if not validate_ip(args.add[0]):
            print("The %s is an invalid IP or Network" % args.add[0])
        else:
            print("%s is a valid IP/Network address" % args.add[0])
    if args.search_note:
        list_by_note(args.search_note)
    if args.search_ip:
        list_by_ip(args.search_ip)
    if args.search_network:
        list_by_network(args.search_network[0])

def validate_ip(ip):
    if not ip:
        return False

    networks = ip.split("/")

    octets = networks[0].split(".")

    if len(octets) > 4:
        return False

    for i in range(0, len(octets)):
        octet = octets[i]
        if not re.match("\d+", octet):
            return False
        octets[i] = int(octet)
        if octets[i] > 255 or octets[i] < 0:
            return False

    if len(networks) == 2:
        if re.match("\d+", networks[1]):
            networks[1] = int(networks[1])
            if networks[1] > 32 or networks[1] < 0:
                return False
        else:
            return False;

    if len(networks) == 1:
        if len(octets) < 4:
            return False
        print("IP address")
    elif len(networks) == 2:
        print("Network address")
    else:
        return False

    return True



def list_infos():
    infos = load_infos()
    print_infos(infos)
    print('Listed %s IPs' % len(infos))

def save_info(ip, note):
    infos = load_infos()

    info = IpInfo(ip, note)
    infos.append(info)
    persist_infos(infos)
    print('\nSaved successfully: %s' % info.to_str())

def list_by_note(note):
    print("Searching for IP with the note '%s'...\n" % note)
    infos = load_infos()
    if len(infos) == 0:
        return

    count = 0
    for info in infos:
        if str(info.note.lower()).find(note.lower()) > -1:
            info.describe()
            count += 1

    print("\n%s IPs found with the note '%s'" % (count, note))

def list_by_ip(address):
    print("Searching for IP containing '%s'...\n" % address)

    infos = load_infos()
    if len(infos) == 0:
        return

    count = 0
    for info in infos:
        if(str(info.ipAddress.lower()).find(address.lower()) > -1):
            info.describe()
            count += 1

    print()
    print("\n%s IPs found with the address '%s'" % (count, address))

def list_by_network(network):
    print("Searching for IP in the network '%s'...\n" % network)

    infos = load_infos()
    if len(infos) == 0:
        return

    count = 0
    for info in infos:
        if str(info.ipAddress).find(network) == 0:
            info.describe()
            count += 1

    print()
    print("\n%s IPs found in the network '%s'" % (count, network))

def load_infos():
    infos = []
    if not os.path.isfile("ip-store.data") or os.path.getsize("ip-store.data") == 0:
        print("No data available.")
    else:
        file = open("ip-store.data", "rb+")
        infos = pickle.load(file)
        if(len(infos) == 0):
            print("There is no IPs saved")
        file.close()
    return infos

def persist_infos(infos):
    file = open('ip-store.data', 'wb+')
    dumped = pickle.dumps(infos)
    file.write(dumped)
    file.close()

if __name__ == '__main__':
    main()