The Nautilus DevOps team wants to install and set up a simple httpd web server on all app servers in Stratos DC. Additionally, they want to deploy a sample web page for now using Ansible only. Therefore, write the required playbook to complete this task. Find more details about the task below.



We already have an inventory file under /home/thor/ansible directory on jump host. Create a playbook.yml under /home/thor/ansible directory on jump host itself.


Using the playbook, install httpd web server on all app servers. Additionally, make sure its service should up and running.


Using blockinfile Ansible module add some content in /var/www/html/index.html file. Below is the content:


Welcome to XfusionCorp!

This is  Nautilus sample file, created using Ansible!

Please do not modify this file manually!


The /var/www/html/index.html file's user and group owner should be apache on all app servers.


The /var/www/html/index.html file's permissions should be 0744 on all app servers.


Note:


i. Validation will try to run the playbook using command ansible-playbook -i inventory playbook.yml so please make sure the playbook works this way without passing any extra arguments.


ii. Do not use any custom or empty marker for blockinfile module.


### solution ###

1) cd /ansible/playbook.yml

2) add this in inventory file
[app_servers]
stapp01 ansible_host=stapp01 ansible_ssh_pass=Ir0nM@n ansible_user=tony
stapp02 ansible_host=stapp02 ansible_ssh_pass=Am3ric@ ansible_user=steve
stapp03 ansible_host=stapp03 ansible_ssh_pass=BigGr33n ansible_user=banner

3) create playbook  
playbook.yml
- name: Install httpd
  hosts: app_servers
  become: yes
  vars:
    httpd_package: "{{ 'httpd' if ansible_facts['os_family'] == 'RedHat' else 'apache2' }}"
    httpd_service: httpd
  tasks:
    - name: Install httpd
      package:
        name: "{{ httpd_package }}"
        state: present
    - name: Start httpd
      service:
        name: "{{ httpd_service }}"
        state: started
        enabled: yes
    - name: Add some contect to index.html
      blockinfile:
        path: /var/www/html/index.html
        block: |
          Welcome to XfusionCorp!
          This is  Nautilus sample file, created using Ansible!
          Please do not modify this file manually!
        create: yes
        group: apache
        owner: apache
        mode: '0744'

4) give access to execute to playbook.yml

run CMD: chmod 744 playbook.yml

5) Run and check everything works
ansible-playbook -i inventory playbook.yml