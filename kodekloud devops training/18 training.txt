xFusionCorp Industries is planning to host a WordPress website on their infra in Stratos Datacenter. They have already done infrastructure configuration—for example, on the storage server they already have a shared directory /vaw/www/html that is mounted on each app host under /var/www/html directory. Please perform the following steps to accomplish the task:



a. Install httpd, php and its dependencies on all app hosts.


b. Apache should serve on port 5004 within the apps.


c. Install/Configure MariaDB server on DB Server.


d. Create a database named kodekloud_db2 and create a database user named kodekloud_sam identified as password 8FmzjvFU6S. Further make sure this newly created user is able to perform all operation on the database you created.


e. Finally you should be able to access the website on LBR link, by clicking on the App button on the top bar. You should see a message like App is able to connect to the database using user kodekloud_sam

######## Solution #########
vvvvvvvvvvvvvvvvvvvvvvvvv

Step a – Install Apache, PHP, and dependencies (on all App hosts)
sudo yum install -y httpd php php-mysqlnd


(If using Ubuntu/Debian:
sudo apt-get install -y apache2 php libapache2-mod-php php-mysql)

Enable and start Apache:

sudo systemctl enable httpd
sudo systemctl start httpd

Step b – Configure Apache to serve on port 5004

Edit Apache configuration file:

sudo vi /etc/httpd/conf/httpd.conf


Find the line:

Listen 80


Change it to:

Listen 5004


Also update any <VirtualHost *:80> block to:

<VirtualHost *:5004>


Then restart Apache:

sudo systemctl restart httpd


Confirm:

sudo netstat -tuln | grep 5004


or

ss -tuln | grep 5004

Step c – Install and configure MariaDB server (on DB host)
sudo yum install -y mariadb-server
sudo systemctl enable mariadb
sudo systemctl start mariadb


Secure the installation (optional but recommended):

sudo mysql_secure_installation

Step d – Create database and user

Log in to MariaDB:

sudo mysql


Then execute:

CREATE DATABASE kodekloud_db2;
CREATE USER 'kodekloud_sam'@'%' IDENTIFIED BY '8FmzjvFU6S';
GRANT ALL PRIVILEGES ON kodekloud_db2.* TO 'kodekloud_sam'@'%';