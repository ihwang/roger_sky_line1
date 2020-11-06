#!/bin/bash
echo $1 | su -c "apt-get upgrade ; apt-get update ; apt-get install sudo -y ; sed -i '20 a "$2"\ \ \ ALL=(ALL:ALL) ALL' /etc/sudoers"