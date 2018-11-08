
import subprocess
import shlex

    
LLDP_CMD = 'lldpctl -f json'
LLDP_CMD = 'cat lldpctl-f.json'

def get_lldpctl():

    lldp_cmd = shlex.split(LLDP_CMD)
    proc = subprocess.Popen('cat lldpctl-f.json', stdout=subprocess.PIPE)

    try:
        (stdout, stderr) = proc.communicate(timeout=20)
    except Exception in (TimeoutExpired):
