# flukepi

An attempt to make a small raspi-based gadget that provides you with
 - LLDP information
 - Link speed/dupex
 - DHCP
 - Speed test against fast.com
 
 ## Install Distro
 Download and install Raspbian stretch lite
 [https://www.raspberrypi.org/downloads/raspbian/]
 
 ## Install latest ansible
 Add the following line to /etc/apt/sources.list:
 ```
 deb http://ppa.launchpad.net/ansible/ansible/ubuntu trusty main
 ```

 Add the repos key and install ansible:
 ```
 sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 93C4A3FD7BB9C367
 sudo apt-get update
 sudo apt-get install ansible
 ```

### Clone the repo
 ```
 git clone https://github.com/itsgc/flukepi.git
 ```
 
### Run Ansible
``` 
sudo ansible-playbook ansible.yml
```

Reboot the device to automatically start the frontend and backend.

