The Nautilus DevOps team needs to copy data from the jump host to all application servers in Stratos DC using Ansible. Execute the task with the following details:


a. Create an inventory file /home/thor/ansible/inventory on jump_host and add all application servers as managed nodes.


b. Create a playbook /home/thor/ansible/playbook.yml on the jump host to copy the /usr/src/itadmin/index.html file to all application servers, placing it at /opt/itadmin.


Note: Validation will run the playbook using the command ansible-playbook -i inventory playbook.yml. Ensure the playbook functions properly without any extra arguments.


#### Solution ###

inventory
[app_servers]
stapp01 ansible_user=tony ansible_ssh_pass=Ir0nM@n ansible_ssh_common_args='-o StrictHostKeyChecking=no'
stapp02 ansible_user=steve ansible_ssh_pass=Am3ric@ ansible_ssh_common_args='-o StrictHostKeyChecking=no'
stapp03 ansible_user=banner ansible_ssh_pass=BigGr33n ansible_ssh_common_args='-o StrictHostKeyChecking=no'


playbook
- name: Copy file to all application servers
  hosts: app_servers
  become: yes

  tasks:
    - name: Ensure destination directory exists
      file:
        path: /opt/itadmin
        state: directory
        mode: '0755'

    - name: Copy file to application servers
      copy:
        src: /usr/src/itadmin/index.html
        dest: /opt/itadmin/index.html
        mode: '0644'

ansible-playbook -i inventory playbook