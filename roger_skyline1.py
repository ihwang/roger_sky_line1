import sys
import json
from os import system,popen


def create_vm(vmname, config):
    is_created = popen("VBoxManage showvminfo " + vmname + " 2>&1 | grep UUID").read()
    if len(is_created) != 0:
        print("roger_skyline1: warning: such virtual machine exists")
        return
    vboxpath = config["vboxpath"] + "/" + vmname + "/" + vmname + ".vdi"
    system("VBoxManage createvm --name " + vmname + " --ostype " \
            + config["ostype"] + " --register")
    system("VBoxManage storagectl " + vmname + " --name IDE --add IDE")
    system("VBoxManage storagectl " + vmname + " --name SATA --add SATA")
    system("VBoxManage storageattach " + vmname \
                    + " --storagectl IDE --port 0 --device 0 --type dvddrive --medium " \
                    + config["isopath"])
    system("VBoxManage createmedium disk --filename " + vboxpath + " --size " + config["disksize"])
    system("VBoxManage storageattach " + vmname \
                  + " --storagectl SATA --port 0 --device 0 --type hdd --medium " \
                  + vboxpath)
    system("VBoxManage modifyvm " + vmname + " --memory 1024 --boot1 dvd --boot2 disk")
    system("VBoxManage modifyvm " + vmname + " --nic1 bridged --bridgeadapter1 en0")
    system("VBoxManage startvm " + vmname)

def config_vm(vmname, config):
    system("VBoxManage startvm " + vmname)

def main(av=sys.argv):
    with open('config.json') as json_config:
        config = json.load(json_config)
    if (len(av) == 1):
        print("roger_skyline1: usage: roger_skyline1   <install|config>")
    elif (av[1] == "install"):
        create_vm(config["vboxname"], config)
    elif (av[1] == "config"):
        config_vm(config["vboxname"], config)

if __name__ == "__main__":
    main()
