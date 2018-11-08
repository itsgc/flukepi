
import subprocess
import shlex
import json


# set type to mock, real, dc
TYPE = 'mock'

if TYPE == 'real':
    LLDP_CMD = 'lldpctl -f json'
elif TYPE == 'mock':
    LLDP_CMD = 'cat test/lldpctl-f.json'
else:
    LLDP_CMD = 'cat test/unplugged.json'


def stderr(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def get_lldpctl():
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


def munge_output(config, interface=u'eth0'):
    '''
    return something like
    { 'switch_name': 'abcdef4-1', 'switch_port': 'xx-0/1/45' }
    but only once since we only have 1 interface
    '''
    base_format = {'switch_name': 'N/A', 'switch_port': 'N/A'}
    # Check if there are any interfaces
    if not config["lldp"].get('interface', False):
        print("Disconnected")
        return False
    base_format['switch_name'] = [ x for x in config["lldp"]["interface"][interface]['chassis']][0]
    id =config["lldp"]["interface"][interface]['port'].get('id', False)
    if id and id['type'] == 'ifname':
        base_format['switch_port'] = id['value']
    else:
        print("Invalid structure")
    return base_format


if __name__ == '__main__':
    config_json = get_lldpctl()
    print(munge_output(config_json))
