#!/usr/bin/env python2

# Integrate with git@github.com:sanderjo/fast.com.git
#   + cloned @ https://github.com/filipposc5/fast.com

# we are doing these shenanigans cos fast.com "package" is python2

from __future__ import print_function
import os

AVAILABLE=False
FAST_PREFIX='../fast'
if os.path.isfile(FAST_PREFIX+'/fast_com.py'):
    if not os.path.islink('fast_com'):
        # print('creating link')
        os.system('ln -sf '+FAST_PREFIX+' fast_com')
    try:
        from fast_com.fast_com import fast_com as speedtest
        AVAILABLE=True
    except:
        pass


def run():
    print(speedtest(verbose=True, maxtime=15, forceipv4=True, forceipv6=False))


if __name__ == '__main__':
    run()
