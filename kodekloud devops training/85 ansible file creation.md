The Nautilus DevOps team is testing various Ansible modules on servers in Stratos DC. They're currently focusing on file creation on remote hosts using Ansible. Here are the details:


a. Create an inventory file ~/playbook/inventory on jump host and include all app servers.


b. Create a playbook ~/playbook/playbook.yml to create a blank file /usr/src/nfsdata.txt on all app servers.


c. Set the permissions of the /usr/src/nfsdata.txt file to 0755.


d. Ensure the user/group owner of the /usr/src/nfsdata.txt file is tony on app server 1, steve on app server 2 and banner on app server 3.


Note: Validation will execute the playbook using the command ansible-playbook -i inventory playbook.yml, so ensure the playbook functions correctly without any additional arguments.


##### solution #####

inventory
    [app_servers]
    stapp01 ansible_user=tony ansible_ssh_pass=Ir0nM@n ansible_ssh_common_args='-o StrictHostKeyChecking=no'
    stapp02 ansible_user=steve ansible_ssh_pass=Am3ric@ ansible_ssh_common_args='-o StrictHostKeyChecking=no'
    stapp03 ansible_user=banner ansible_ssh_pass=BigGr33n ansible_ssh_common_args='-o StrictHostKeyChecking=no'

Verify CMD: ansible -i inventory app_servers -m ping

# Create playbook names playbook.ymls
playbook.yml
- name: create black file
  hosts: app_servers
  become: yes
  tasks:
    - name: ensure desination file exists
      file:
        path: /opt
        state: directory

    - name: create empty file
      file:
        path: /opt/nfsdata.txt
        state: touch
        mode: '0655'
        owner: "{{ ansible_user }}"
        group: "{{ ansible_user }}"


ansible-playbook -i inventory playbook.yml