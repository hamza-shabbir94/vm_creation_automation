from termcolor import cprint
import os, shutil
# get the info from the client

# update the list according to the operation_systems options based on the templates's name
all_operating_systems = ["ubuntu20", "windows2019"]
ansible_directory = "./Ansible"
inventory_file = "./Ansible/Inventories/Hosts1"

# getting the variables needed for the VM
vm_name=str(input("The name of the VM: "))
vm_ram=int(input("The Ram for the VM in MB: "))
vm_cpu=int(input("Number of CPU cores: "))
vm_disk=int(input("The disk for the server in GB: "))
vm_ip=str(input("Please type the IP which should be assigned to this VM: "))
for id,os in enumerate(all_operating_systems):
    print(f"{id + 1}- {os}")
os_option=int(input("choose the OS of the VM (number only): "))

if os_option > len(all_operating_systems):
    print("wrong input for the operating system")
    exit(1)
else:
    pass

vm_node = str(input("type the node name for this server: "))

cprint(f"""this vm will have:
    Name: {vm_name}
    Ram: {vm_ram} MB
    Cpu: {vm_cpu} Cores
    disk: {vm_disk} GB
    OS: {all_operating_systems[os_option - 1]}
    Node: {vm_node}
        """, color="yellow")

confirmed = str(input("type y or yes if above VM is what you are looking for: ")).lower()
if confirmed == "y" or confirmed == "yes":
    print("------")
    pass
else:
    print("exiting... ")
    exit(1)
##################################
# Program starts from below #
##################################

# functions
def create_vm(vm_name):
    open_curly_braces = "{{"
    close_curly_braces = "}}"
    with open(f"{ansible_directory}/{vm_name}.yaml", "w+") as vm_file:
        content = f"""---
- hosts: {vm_name}
  gather_facts: false
  roles: 
    - role: create_linux_vm
      node: "{open_curly_braces} hostvars.{vm_name}.node {close_curly_braces}"
      vm_name: "{open_curly_braces} hostvars.{vm_name}.name {close_curly_braces}"
      vm_disk: "{open_curly_braces} hostvars.{vm_name}.disk {close_curly_braces}"
      vm_template: "{open_curly_braces} hostvars.{vm_name}.template {close_curly_braces}"
      vm_datastore: "{open_curly_braces} hostvars.{vm_name}.datastore {close_curly_braces}"
      vm_memory: "{open_curly_braces} hostvars.{vm_name}.memory {close_curly_braces}"
      vm_cpu: "{open_curly_braces} hostvars.{vm_name}.cpu {close_curly_braces}"
      vm_network1_name: "{open_curly_braces} hostvars.{vm_name}.network1_name {close_curly_braces}"
      vm_network1_ip: "{open_curly_braces} hostvars.{vm_name}.network1_ip {close_curly_braces}"
      vm_network1_netmask: "{open_curly_braces} hostvars.{vm_name}.network1_subnet {close_curly_braces}"
      vm_network1_gateway: "{open_curly_braces} hostvars.{vm_name}.network1_gateway {close_curly_braces}"

- hosts: {vm_name}
  gather_facts: true
  roles:
    - role: extend-linux-disk
      disk_size: "{open_curly_braces} hostvars.{vm_name}.disk {close_curly_braces}"
    - role: ssh-pubkey
      key_file:
        - faridsaadat_pubkey
        - hamza_pubkey
    - role: set-timezone
      zone: UTC
    - role: linux-initial-config \n"""
        vm_file.writelines(content)
        vm_file.close()
        print(f"{vm_name}.yaml generated successfully.")

##################################
# steps for the code #
##################################
# update host_vars folder in Inventories with provided information
with open(f"./Ansible/Inventories/host_vars/{vm_name}.yaml", "w+") as vminventoryyaml:
    vminventoryyaml.write(f"""ansible_host: {vm_ip}
ram: {vm_ram}
cpu: {vm_cpu}
disk: {vm_disk}
os: {all_operating_systems[os_option - 1]}
ip: {vm_ip}
node: { vm_node }
""")
    vminventoryyaml.close()

with open(inventory_file, "r+") as inventoryfile:
    lines = inventoryfile.readlines()
    new_line = f"{vm_name} \n"
    if new_line in lines:
        cprint(f"host {vm_name} already exists... try changing it's name to another thing", "red")
        exit(1)
    else:
        inventoryfile.write(new_line)
        cprint(f"{vm_name} added to inventory was successful.", "green")

create_vm(vm_name=vm_name)
