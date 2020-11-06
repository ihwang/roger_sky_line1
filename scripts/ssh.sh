#!/bin/bash
sshd_config=/etc/ssh/sshd_config
echo $1 | sudo -S sed -i '13,13d' $sshd_config; sudo sed -i '13 a Port '$2 $sshd_config
echo $1 | sudo -S sed -i '32,32d' $sshd_config; sudo sed -i '32 a PermitRootLogin no' $sshd_config
sudo service ssh restart