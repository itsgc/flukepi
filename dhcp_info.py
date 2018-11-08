
import subprocess
import shlex
import json
import re
import struct
from socket import AF_INET
from socket import inet_ntoa
from pyroute2 import IPRoute
from pyroute2 import NetNS
from pyroute2 import IPDB

# get access to the netlink socket

def cidr_to_netmask(cidr):
    host_bits = 32 - int(cidr)
    netmask = inet_ntoa(struct.pack('!I', (1 << 32) - (1 << host_bits)))
    return netmask


def stderr(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def get_ipaddr_data(response_type):
    if response_type == 'real':
        # ip = IPRoute()
        with NetNS('dp') as ip:
            try:
                interface = ip.get_addr(label='eth0', family=AF_INET)
                ip_address = interface[0].get_attr('IFA_ADDRESS')
                cidr = interface[0]['prefixlen']
                gateway = ip.get_default_routes(family=AF_INET)[0].get_attr('RTA_GATEWAY')
            except Exception as e:
                raise e
    elif response_type == 'mock':
        ip_address = '192.168.0.5'
        cidr = 24
        gateway = '192.168.0.1' 
    else:
        ip_address = 'N/A'
        cidr = 0
        gateway = 'N/A'
 
    j = { 'ip_address': ip_address,
          'subnet_mask': cidr_to_netmask(cidr),
          'gateway': gateway }
    return j

def munge_output(config):
    '''
    return something like
    { 'gateway': '172.16.0.1', 'ip_address': '172.16.0.6', 'subnet_mask': '255.255.255.0' }
    but only once since we only have 1 interface
    '''
    base_format = {
                    'gateway': 'N/A',
                    'ip_address': 'N/A',
                    'subnet_mask': 'N/A'
                  }
    base_format['ip_address'] = config['ip_address']
    base_format['subnet_mask'] = config['subnet_mask']
    base_format['gateway'] = config['gateway']
    return base_format


def get_dhcp_info(response_type='real'):
    if response_type not in [ 'mock', 'real' ]:
        raise "Invalid response type"
    config = get_ipaddr_data(response_type)
    return munge_output(config)


if __name__ == '__main__':
    print(json.dumps(get_dhcp_info()))

