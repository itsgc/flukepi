
import subprocess
import shlex
import json
import re


def stderr(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def get_lldpctl(response_type):
    if response_type == 'real':
        LLDP_CMD = 'lldpctl -f json'
    elif response_type == 'mock':
        LLDP_CMD = 'cat test/lldpctl-f.json'
    else:
        LLDP_CMD = 'cat test/unplugged.json'
    lldp_cmd = shlex.split(LLDP_CMD)
    proc = subprocess.Popen(lldp_cmd, stdout=subprocess.PIPE)

    try:
        (stdout, stderr) = proc.communicate(timeout=20)
    except (TimeoutExpired) as e:
        stderr(e.msg)
        return False
    j = json.loads(stdout.decode('utf-8'))
    # json.dumps(j, sort_keys=True, indent=2)
    return j

def vlan_lookup(lookuptable='/etc/vlan_lookup.json', vlan_id=None):
    try:
      with open(lookuptable) as json_data:
          d = json.load(json_data)
      print(vlan_id)
      value = d[vlan_id] + "(" + vlan_id + ")"
      return value
    except FileNotFoundError as e:
      value = vlan_id
      return value
    except KeyError as e:
      value = None
      return value
    except Exception as e:
      raise e

def munge_output(config, interface=u'eth0'):
    '''
    return something like
    { 'switch_name': 'abcdef4-1', 'switch_port': 'xx-0/1/45', 'vlans':[]}
    but only once since we only have 1 interface
    '''
    base_format = {
                    'switch_name': 'N/A',
                    'switch_port': 'N/A',
                    'vlans': []
                  }
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
            vlan_lookup(vlan_id=v['vlan-id']) for v in vlans if ( v['value'] != 'vlan-1' and v['value'] != 'voice' )]
    return base_format


def get_lldp_info(response_type='real'):
    if response_type not in [ 'mock', 'real', 'dc' ]:
        raise "Invalid response type"
    config_json = get_lldpctl(response_type)
    return munge_output(config_json)


if __name__ == '__main__':
    print(get_lldp_info(response_type='real'))
