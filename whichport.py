from scapy.all import *
from scapy.all import *
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

load_contrib('lldp')
def lldp_callback(pkt):
	switch = pkt[LLDPDU][LLDPDUSystemName].system_name
	port = pkt[LLDPDU][LLDPDUPortID].id
	# vlan = pkt[LLDPDU]
	# orgspecific = vlan[LLDPDUGenericOrganisationSpecific]
	# print orgspecific.show()
	print "This machine is currently on: {} port {}".format(switch, port)
	# pkt.display()

sniff(prn=lldp_callback, iface="en7", filter="ether proto 0x88cc", store=0)
