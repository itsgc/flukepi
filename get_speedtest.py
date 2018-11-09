
import io
import subprocess
from queue import Queue
from threading import Thread
from time import sleep


def run_process(cmd, queue):
    #proc = subprocess.Popen([""], stdout=subprocess.PIPE)
    with subprocess.Popen(cmd, stdout=subprocess.PIPE) as proc:
        for line in io.TextIOWrapper(proc.stdout, encoding="utf-8"):
            if 'Loop' in line:
                queue.put(line.strip())


def worker(cmd_q):
    global started
    while True:
        if started:
            print(cmd_q.get())
        time.sleep(0.2)




if __name__ == '__main__':
    started = False
    cmd = ["./long-cmd"]
    cmd = ["python2", "-u", "fast_integration_py2.py" ]
    q = Queue()
    t = Thread(target=worker, args=(q,))
    t.daemon = True
    t.start()
    run_process(cmd, q)
