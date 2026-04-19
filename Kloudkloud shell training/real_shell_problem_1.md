We have one of our websites up and running on our Nautilus infrastructure in Stratos DC. Our security team has raised a concern that right now Apache’s port i.e 5004 is open for all since there is no firewall installed on these hosts. So we have decided to add some security layer for these hosts and after discussions and recommendations we have come up with the following requirements:


1. Install iptables and all its dependencies on each app host.


2. Block incoming port 5004 on all apps for everyone except for LBR host.


3. Make sure the rules remain, even after system reboot.

-------------------- SOLUTION --------------------
||||||||||||||||||||||||||||||||||||||||||||||||||

Perfect — this is a classic iptables + persistence exercise. Let’s do it step by step.

1. Install iptables
On each app host (e.g., stapp01, stapp02, stapp03):

For CentOS/RHEL:

bash
Copy
Edit
sudo yum install -y iptables-services
For Ubuntu/Debian:

bash
Copy
Edit
sudo apt update
sudo apt install -y iptables-persistent
2. Block incoming port 8082 for everyone except LBR
Assume LBR host IP = <LBR_IP> (replace with the actual IP of the Load Balancer host).

Run on each app host:

bash
Copy
Edit
# Allow LBR to connect on 8082
sudo iptables -A INPUT -p tcp -s <LBR_IP> --dport 8082 -j ACCEPT

# Block everyone else on 8082
sudo iptables -A INPUT -p tcp --dport 8082 -j DROP
Order matters: put the ACCEPT rule above the DROP rule.

3. Save rules permanently
CentOS/RHEL:
bash
Copy
Edit
# Save rules
sudo service iptables save

# Enable iptables service on boot
sudo systemctl enable iptables
sudo systemctl restart iptables
Rules are stored in /etc/sysconfig/iptables.

Ubuntu/Debian:
During installation of iptables-persistent, it usually asks to save current rules.
If not, run:

bash
Copy
Edit
sudo netfilter-persistent save
sudo netfilter-persistent enable
Rules are saved in /etc/iptables/rules.v4.

4. Verify
Check active rules:

bash
Copy
Edit
sudo iptables -L -n -v
Test from:

LBR host → should connect to port 8082.

Other hosts → should get blocked.

