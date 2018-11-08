
import re
import subprocess
import shlex

def stderr(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def get_ethtool(response_type):
    if response_type == 'real':
       ETHTOOL_CMD = 'ip netns exec dp ethtool eth0'
    elif response_type == 'mock':
       ETHTOOL_CMD = 'cat test/ethtool.txt'
    else:
       ETHTOOL_CMD = 'cat test/unplugged.json'
    ethtool_cmd = shlex.split(ETHTOOL_CMD)
    proc = subprocess.Popen(ethtool_cmd, stdout=subprocess.PIPE)

    try:
        (stdout, stderr) = proc.communicate(timeout=20)
    except (TimeoutExpired) as e:
        stderr(e.msg)
        return False
    #j = json.loads(stdout.decode('utf-8'))
    j = stdout.decode('utf-8')
    # json.dumps(j, sort_keys=True, indent=2)
    return j


def munge_output(config, interface=u'eth0'):
    '''
    return something like
    { 'speed': '1000Mb/s', 'duplex': 'Full'}
    but only once since we only have 1 interface
    '''
    base_format = {
                    'speed': 'N/A',
                    'duplex': 'N/A'
                  }
    '''
    # Check if there are any interfaces
    if not config["lldp"].get('interface', False):
        print("Disconnected")
        return False
    switches = [x for x in config["lldp"]["interface"][interface]['chassis']]
    if len(switches) > 1:
        stderr("MORE THAN ONE SWITCHES DETECTED")
    # We have only 1 port so just get the 1st switch
    base_format['switch_name'] = switches[0]
    id = config["lldp"]["interface"][interface]['port'].get('id', False)
    if id and id['type'] == 'ifname':
        base_format['switch_port'] = id['value']
    else:
        print("Invalid structure")
    vlans = config['lldp']['interface'][interface].get('vlan', False)
    if vlans:
        base_format['vlans'] += [
            v['value'] for v in vlans if v['value'] != 'vlan-1']
    return base_format
    '''
    for line in config.splitlines():
        #print(line)
        if "Speed:" in line: base_format['speed'] = re.sub(r"[\t]*", "", line)
        if "Duplex:" in line: base_format['duplex'] = re.sub(r"[\t]*", "", line)

    return base_format 

def get_ethtool_info(response_type='real'):
    if response_type not in [ 'mock', 'real', 'dc' ]:
        raise "Invalid response type"
    result_txt = get_ethtool(response_type)
    return munge_output(result_txt)


if __name__ == '__main__':
    print(get_ethtool_info(response_type='mock'))
