Developers are looking for dependencies to be installed and run on Nautilus app servers in Stratos DC. They have shared some requirements with the DevOps team. Because we are now managing packages installation and services management using Ansible, some playbooks need to be created and tested. As per details mentioned below please complete the task:



a. On jump host create an Ansible playbook /home/thor/ansible/playbook.yml and configure it to install httpd on all app servers.


b. After installation make sure to start and enable httpd service on all app servers.


c. The inventory /home/thor/ansible/inventory is already there on jump host.


d. Make sure user thor should be able to run the playbook on jump host.


Note: Validation will try to run playbook using command ansible-playbook -i inventory playbook.yml so please make sure playbook works this way, without passing any extra arguments.

## solution

1) inventory
[app_servers]
stapp01 ansible_host=stapp01 ansible_ssh_pass=Ir0nM@n ansible_user=tony
stapp02 ansible_host=stapp02 ansible_ssh_pass=Am3ric@ ansible_user=steve
stapp03 ansible_host=stapp03 ansible_ssh_pass=BigGr33n ansible_user=banner

2) playbook.yml
- name: Install httpd
  hosts: app_servers
  become: yes
  vars:
    httpd_package: "{{ 'httpd' if ansible_facts['os_family'] == 'RedHat' else 'apache2' }}"
    httpd_service: httpd
  tasks:
    - name: Install httpd package
      yum:
        name: "{{ httpd_package }}"
        state: present
    - name: Start httpd Service
      service:
        name: "{{ httpd_service  }}"
        state: started
        enabled: yes

3) chmod 744 playbook.yml