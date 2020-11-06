#!/bin/bash
netConfigFile=/etc/network/interfaces.d/enp0s3
echo $1 | sudo -S sed -i '11,12d' /etc/network/interfaces ; sudo sed -i '10 a auto\ enp0s3' /etc/network/interfaces
echo $1 | sudo -S bash -c "echo iface enp0s3 inet static > /etc/network/interfaces.d/enp0s3"
echo $1 | sudo -S sed -i '1 a address '$2 $netConfigFile
echo $1 | sudo -S sed -i '2 a netmask '$3 $netConfigFile
echo $1 | sudo -S sed -i '3 a gateway '$4 $netConfigFile
sudo service networking restart