import sys
import json
from time import sleep
from os import system,popen


def create_vm(vmname, config):
    is_created = popen("VBoxManage showvminfo " + vmname + " 2>&1 | grep UUID").read()
    if len(is_created) != 0:
        print("roger_skyline1: warning: such virtual machine exists", file=sys.stderr)
        return
    system("mv preseed.cfg " + config["isodirectory"])
    vboxpath = config["vboxpath"] + "/" + vmname + "/" + vmname + ".vdi"
    system("VBoxManage createvm --name " + vmname + " --ostype " \
            + config["ostype"] + " --register")
    system("VBoxManage storagectl " + vmname + " --name IDE --add IDE")
    system("VBoxManage storagectl " + vmname + " --name SATA --add SATA")
    system("VBoxManage storageattach " + vmname \
                    + " --storagectl IDE --port 0 --device 0 --type dvddrive --medium " \
                    + config["isodirectory"] + "/")
    system("VBoxManage createmedium disk --filename " + vboxpath + " --size " + config["disksize"])
    system("VBoxManage storageattach " + vmname \
                  + " --storagectl SATA --port 0 --device 0 --type hdd --medium " \
                  + vboxpath)
    system("VBoxManage modifyvm " + vmname + " --memory 1024 --boot1 dvd --boot2 disk")
    system("VBoxManage modifyvm " + vmname + " --nic1 bridged --bridgeadapter1 en0")
    system("VBoxManage startvm " + vmname)

def config_net(config):
    sleep(1)
    system("ssh -p " + config["port"] + " " + config["username"] + "@" + config["ip"] + \
            " 'sh -s' < scripts/network.sh " + config["passwd"] + " " + config["ip"] + " " + \
            config["netmask"] + " " + config["gateway"])
    print("\nroget_skyline1: network configuration is successfully done")

def config_ssh(config):
    sleep(1)
    system("ssh " + config["username"] + "@" + config["ip"] + " 'sh -s' < scripts/ssh.sh " + \
            config["passwd"] + " " + config["port"])
    print("\nroget_skyline1: ssh configuration is successfully done")

def install_pkgs(config):
    system("ssh " + config["username"] + "@" + config["ip"] + " 'sh -s' < scripts/pkgs.sh " + \
            config["passwd"] + " " + config["username"])
    print("roget_skyline1: necessary packages are successfully installed")

def config_vm(vmname, config):
    is_running = popen("VBoxManage showvminfo " + vmname + " | grep running").read()
    if (len(is_running)) == 0:
        print("roger_skyline1: warning: run the vm you want to configure", file=sys.stderr)
        return
    system("ssh-keygen -t rsa")
    system("echo " + config["passwd"] + " | ssh-copy-id -i ~/.ssh/id_rsa " + config["username"] + "@" + config["ip"])
    install_pkgs(config)
    config_ssh(config)
    config_net(config)

def main(av=sys.argv):
    with open('config.json') as json_config:
        config = json.load(json_config)
    if (len(av) == 1):
        print("roger_skyline1: usage: roger_skyline1   <install|config>", file=sys.stderr)
    elif (av[1] == "install"):
        create_vm(config["vboxname"], config)
    elif (av[1] == "config"):
        config_vm(config["vboxname"], config)

if __name__ == "__main__":
    main()
