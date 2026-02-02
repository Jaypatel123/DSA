An Ansible playbook needs completion on the jump host, where a team member left off. Below are the details:



The inventory file /home/thor/ansible/inventory requires adjustments. The playbook must run on App Server 2 in Stratos DC. Update the inventory accordingly.


Create a playbook /home/thor/ansible/playbook.yml. Include a task to create an empty file /tmp/file.txt on App Server 2.


Note: Validation will run the playbook using the command ansible-playbook -i inventory playbook.yml. Ensure the playbook works without any additional arguments.


##### solution 

inventory file
    stapp02 ansible_host=172.16.238.11 ansible_user=steve ansible_ssh_common_args='-o StrictHostKeyChecking=no' ansible_ssh_pass=Am3ric@


playbook.yml:
    - name: create file
      hosts: stapp02
      become: yes
      tasks:
          - name: Create an empty file
          file:
              path: /tmp/file.txt
              state: touch


run playbooks cmd: 
    ansible-playbook -i inventory playbook.yml