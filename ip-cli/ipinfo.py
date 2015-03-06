__author__ = 'Leonardo Rafaeli'
import pickle
import os
from argparse import ArgumentParser
from collections import defaultdict
import re
import pprint


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
    parser.add_argument("-si", "--search-ip", help="Search IP by address or by Network", metavar="IP OR NETWORK IN CIDR")

    args = parser.parse_args()

    if args.list:
        list_infos()
    elif args.add:
        save_info(args.add[0], " ".join(args.add[1:]))
    elif args.search_note:
        list_by_note(args.search_note)
    elif args.search_ip:
        list_by_ip(args.search_ip)
    else:
        parser.print_help()


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
        print("IP address received\n")
    elif len(networks) == 2:
        print("Network address received\n")
    else:
        return False

    return True


def list_infos():
    infos = load_infos()

    print_infos(infos)
    print('Listed %s IPs' % len(infos))


def save_info(ip, note):
    if not validate_ip(ip):
        print("The %s is an invalid IP or Network" % ip)
        return
    else:
        print("%s is a valid IP/Network address" % ip)

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

    if not validate_ip(address):
        print("%s is an invalid IP or Network address" % address)
        return

    infos = load_infos()

    if len(infos) == 0:
        print("No IP was found because the database is empty")
        return

    tree = create_address_tree(infos)

    found_infos = find_ip_in_tree(tree, address)
    print_infos(found_infos)
    print("\n%s IPs found with the address '%s'" % (len(found_infos), address))


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
        if (len(infos) == 0):
            print("There is no IPs saved")
        file.close()
    return infos


def persist_infos(infos):
    file = open('ip-store.data', 'wb+')
    dumped = pickle.dumps(infos)
    file.write(dumped)
    file.close()


def create_address_tree(infos):
    root = {}
    for info in infos:
        network = info.ipAddress.split('/')
        octets = network[0].split('.')

        last_dict = {}
        i = len(octets) - 1
        while i >= 0:
            octet = octets[i]
            info_dict = {}
            if i == len(octets) - 1:
                if len(network) == 2:
                    info_dict["/" + network[1]] = {'note': info.note}
                else:
                    info_dict[octet] = {'note': info.note}
                last_dict = info_dict
                i -= 1
                continue
            if i == 0:
                info_dict[octet] = last_dict
                last_dict = info_dict

                add_in_tree(root, last_dict)
            else:
                info_dict[octet] = last_dict
                last_dict = info_dict
            i -= 1

    return root


def add_in_tree(tree, node):
    d_tree = defaultdict(lambda: None, tree)
    for key in node.keys():
        if d_tree[key]:
            add_in_tree(tree[key], defaultdict(lambda: None, node[key]))
        else:
            tree.update({key: defaultdict(lambda: None, node[key])})
            break


def find_ip_in_tree(tree, ip):
    default_tree = defaultdict(lambda: None, tree)

    network = ip.split("/")
    octets = network[0].split(".")

    result = []

    i = 0
    last_tree = {}
    ip_found = ""
    while i < len(octets):
        octet = octets[i]
        if i == 0:
            if default_tree[octet]:
                last_tree = defaultdict(lambda: None, default_tree[octet])
                i += 1
                ip_found = octet

                if len(octets) == 1:
                    list_all_keys(last_tree, ip_found, result)
                    break

                continue
            else:
                break

        if last_tree[octet]:
            ip_found = ip_found + "." + octet
            last_tree = defaultdict(lambda: None, last_tree[octet])
            if i == len(octets) - 1:
                if len(network) == 2:
                    print("Listing all networks under " + ip_found + "/" + network[1] + "\n")
                    list_all_keys(last_tree, ip_found, result)
                    break;
                else:
                    result.append(IpInfo(ip_found, last_tree["note"]))
            else:
                i += 1
                continue
        else:
            break

    return result


def list_all_keys(node, desc, result):
    for a, b in node.items():
        if "note" == a:
            result.append(IpInfo(desc, b))
        else:
            list_all_keys(node[a], desc + "." + a, result)


if __name__ == '__main__':
    main()