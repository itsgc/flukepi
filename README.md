# lldp_pokedex

an attempt to make a small raspi-based gadget that tells you LLDP information and possibly link speed / dhcp etc.

Add the following line to /etc/apt/sources.list:

deb http://ppa.launchpad.net/ansible/ansible/ubuntu trusty main
Then run these commands:

sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 93C4A3FD7BB9C367
sudo apt-get update
sudo apt-get install ansible


Start backend
sudo uwsgi --ini uwsgi.ini

Start Frontend
sudo python3 pydisplay.py
