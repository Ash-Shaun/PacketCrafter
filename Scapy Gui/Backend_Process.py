import netifaces
from scapy.all import *
from temp import text

IP_addr = ['172.18.0.1', '172.19.0.1', '172.17.0.1', '192.168.38.138', '127.0.0.1']
MAC = ['00:0c:29:79:14:67', '00:00:00:00:00:00', '02:42:2b:9e:1a:6d', '02:42:11:16:25:ea', 'ff:ff:ff:ff:ff:ff']


def getinterfaces():
    iface = netifaces.interfaces()
    return iface

def arp_send(ifc,IP,a):
    if a is False:
        success, fail = srp(Ether(dst = "ff:ff:ff:ff:ff:ff")/ARP(pdst = IP), timeout = 2, iface = ifc, inter = 0.1)
    else:
        success, fail = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=IP, op = 2), timeout=2, iface=ifc, inter=0.1)
    return success

def ip_header(ethsrc,ethdst,ipsrc,ipdst,ifc):
    a = Ether(src = ethsrc, dst = ethdst)/IP(src = ipsrc, dst = ipdst)
    success, fail = srp(a, iface= ifc, timeout= 2)
    return success

def eth(source,dest,ifc):
    success, fail= srp(Ether(src = source, dst= dest),iface= ifc, timeout=2)
    return  success

def transport_layer(protocol, portsrc, portdst, flag, payload, ipsrc, ipdes, ifc):
    if protocol == "ICMP":
        text = 'success, fail = srp(IP(src = "{}", dst = "{}")/ICMP(), timeout = 2, iface = "{}")'.format(ipsrc, ipdes, ifc)
    elif protocol == "TCP":
        text = 'success, fail = srp(IP(src = "{}", dst = "{}")/TCP(sport = {}, dport = {}, flags = "{}"), timeout = 2, iface = "{}")'.format(ipsrc,ipdes,portsrc,portdst,flag,iface)
    elif protocol == "UDP":
        text = 'success, fail = srp(IP()/UDP())'
    return text

