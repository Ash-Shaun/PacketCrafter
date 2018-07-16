def Ether_header(sr = "", ds="ff:ff:ff:ff:ff:ff", ifc =""):
    if sr == "":
        if ds == '' or ds =="ff:ff:ff:ff:ff:ff":
            a = '''A = Ether()''' + "\n" + "sendp(A, iface = \"{}\")".format(ifc)
        else:
            a = 'A = Ether(dst="'+ ds + '")'+ "\n" + "sendp(A, iface = \"{}\")".format(ifc)
        return a
    else:
        a = 'A = Ether(src="' + sr + '", dst="' + ds + '")' + "\n" + "sendp(A, iface = \"{}\")".format(ifc)
        if ds == "":
            a = 'A = Ether(src="' + sr + '",dst="ff:ff:ff:ff:ff:ff")' + "\n" + "sendp(A, iface = \"{}\")".format(ifc)
        return(a)

def ip_header(ethsrc,ethdst,ipsrc,ipdst,ifc):
    a = 'A = Ether(src = "{}", dst = "{}")/IP(src = "{}", dst = "{}")'.format(ethsrc,ethdst,ipsrc,ipdst)
    snd = "sendp(A, iface = \"{}\")".format(ifc)
    result = a + "\n" + snd
    return result

def arp_code(ifc,IP,a):
    if a is False:
        text = 'success, fail = srp(Ether(dst = "ff:ff:ff:ff:ff:ff")/ARP(pdst = "{}", op = 1), timeout = 2, iface = "{}", inter = 0.1)'.format(IP,ifc)
    else:
        text = 'success, fail = srp(Ether(dst = "ff:ff:ff:ff:ff:ff")/ARP(pdst = "{}", op = 2), timeout = 2, iface = "{}", inter = 0.1)'.format(IP, ifc)
    return text

def transport_layer(protocol, portsrc, portdst, flag, payload, ipsrc, ipdes, ifc):
    if protocol == "ICMP":
        text = 'success, fail = srp(IP(src = "{}", dst = "{}")/ICMP(), timeout = 2, iface = "{}")'.format(ipsrc, ipdes, ifc)
    elif protocol == "TCP":
        text = 'success, fail = srp(IP(src = "{}", dst = "{}")/TCP(sport = {}. dport = {}, flags = "{}"), timeout = 2, iface = "{}")'.format(ipsrc,ipdes,portsrc,portdst,flag,ifc)
    elif protocol == "UDP":
        text = 'success, fail = srp(IP()/UDP())'
    return text

