Following security audits, the xFusionCorp Industries security team has rolled out new protocols, including the restriction of direct root SSH login.


Your task is to disable direct SSH root login on all app servers within the Stratos Datacenter.

-------- Solution ------------

# Open the SSH configuration file
sudo vi /etc/ssh/sshd_config

# mark permit no to root access
PermitRootLogin no

sudo systemctl restart sshd


