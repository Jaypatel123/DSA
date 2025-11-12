xFusionCorp Industries is planning to host two static websites on their infra in Stratos Datacenter. The development of these websites is still in-progress, but we want to get the servers ready. Please perform the following steps to accomplish the task:



a. Install httpd package and dependencies on app server 1.


b. Apache should serve on port 6400.


c. There are two website's backups /home/thor/media and /home/thor/games on jump_host. Set them up on Apache in a way that media should work on the link http://localhost:6400/media/ and games should work on link http://localhost:6400/games/ on the mentioned app server.


d. Once configured you should be able to access the website using curl command on the respective app server, i.e curl http://localhost:6400/media/ and curl http://localhost:6400/games/


######### Solution ############
vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv


sudo scp -r /home/thor/media /home/thor/games tony@172.16.238.10:/tmp/

ssh tony@172.16.238.10

sudo yum install httpd -y 

sudo vi /etc/httpd/conf/httpd.conf

    change port Listen 80 port to Listen 6400

sudo rm /etc/httpd/conf.d/welcome.conf

sudo systemctl restart httpd

sudo systemctl enable httpd

