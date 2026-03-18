The Nautilus Application development team wanted to test some applications on app servers in Stratos Datacenter. They shared some pre-requisites with the DevOps team, and packages need to be installed on app servers. Since we are already using Ansible for automating such tasks, please perform this task using Ansible as per details mentioned below:



Create an inventory file /home/thor/playbook/inventory on jump host and add all app servers in it.


Create an Ansible playbook /home/thor/playbook/playbook.yml to install chrony package on all  app servers using Ansible yum module.


Make sure user thor should be able to run the playbook on jump host.

Note: Validation will try to run playbook using command ansible-playbook -i inventory playbook.yml so please make sure playbook works this way, without passing any extra arguments.


### Solution ###

inventory
    [all_servers]
    stapp01 ansible_user=tony ansible_ssh_pass=Ir0nM@n ansible_ssh_common_args='-o StrictHostKeyChecking=no'
    stapp02 ansible_user=steve ansible_ssh_pass=Am3ric@ ansible_ssh_common_args='-o StrictHostKeyChecking=no'
    stapp03 ansible_user=banner ansible_ssh_pass=BigGr33n ansible_ssh_common_args='-o StrictHostKeyChecking=no'

playbook.yum
    - name: Install chrony
    hosts: all_servers
    become: yes
    tasks:
        - name: Install chrony package
        ansible.builtin.yum:
            name: chrony
            state: present