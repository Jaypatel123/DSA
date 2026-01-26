The Nautilus development team had a meeting with the DevOps team where they discussed automating the deployment of one of their apps using Jenkins (the one in Stratos Datacenter). They want to auto deploy the new changes in case any developer pushes to the repository. As per the requirements mentioned below configure the required Jenkins job.


Click on the Jenkins button on the top bar to access the Jenkins UI. Login using username admin and Adm!n321 password.


Similarly, you can access the Gitea UI using Gitea button, username and password for Git is sarah and Sarah_pass123 respectively. Under user sarah you will find a repository named web that is already cloned on the Storage server under sarah's home. sarah is a developer who is working on this repository.


1. Install httpd (whatever version is available in the yum repo by default) and configure it to serve on port 8080 on All app servers. You can make it part of your Jenkins job or you can do this step manually on all app servers.


2. Create a Jenkins job named nautilus-app-deployment and configure it in a way so that if anyone pushes any new change to the origin repository in master branch, the job should auto build and deploy the latest code on the Storage server under /var/www/html directory. Since /var/www/html on Storage server is shared among all apps.
Before deployment, ensure that the ownership of the /var/www/html directory is set to user sarah, so that Jenkins can successfully deploy files to that directory.


3. SSH into Storage Server using sarah user credentials mentioned above. Under sarah user's home you will find a cloned Git repository named web. Under this repository there is an index.html file, update its content to Welcome to the xFusionCorp Industries, then push the changes to the origin into master branch. This push must trigger your Jenkins job and the latest changes must be deployed on the servers, also make sure it deploys the entire repository content not only index.html file.

Click on the App button on the top bar to access the app, you should be able to see the latest changes you deployed. Please make sure the required content is loading on the main URL https://<LBR-URL> i.e there should not be any sub-directory like https://<LBR-URL>/web etc.


Note:
1. You might need to install some plugins and restart Jenkins service. So, we recommend clicking on Restart Jenkins when installation is complete and no jobs are running on plugin installation/update page i.e update centre. Also some times Jenkins UI gets stuck when Jenkins service restarts in the back end so in such case please make sure to refresh the UI page.


2. Make sure Jenkins job passes even on repetitive runs as validation may try to build the job multiple times.


3. Deployment related tasks should be done by sudo user on the destination server to avoid any permission issues so make sure to configure your Jenkins job accordingly.


4. For these kind of scenarios requiring changes to be done in a web UI, please take screenshots so that you can share it with us for review in case your task is marked incomplete. You may also consider using a screen recording software such as loom.com to record and share your work.



######## Solution ########

update jenkins:
manage jenkins > plugins > updates > check all plugins > click Install > restart jenkins

Install necessary plugins:
manage jenkins > plugins > available plugins > ssh, SSH Credentials, SSH Build Agents, gitea > restart jenkins 

Add Credentials:
manage jenkins > credentials > 
                    steve, 
                    banner, 
                    tony, and 
                    natasha,

Add ssh host:
    manage Jenkins > system > SSH > 
                            add steve, tony, banner, natasha hostnames with Port 22 & attach credentials for all respective servers > save 

Create a Job to install httpd and changing the apache port to 8080
    Job> Name: httpd > FreeStyle > Build Steps > open three seperate "Execute shell script on remote host using ssh" > for all three select tony, steve and banner in SSH sites > 
        First script
            echo "Ir0nM@n" | sudo -S yum install httpd -y
            echo "Ir0nM@n" | sudo -S sed -i 's/^Listen[[:space:]]\+[0-9]\+/Listen 8080/' /etc/httpd/conf/httpd.conf
            cat /etc/httpd/conf/httpd.conf | grep Listen
            echo "Ir0nM@n" | sudo -S systemctl start httpd
            echo "Ir0nM@n" | sudo -S systemctl enable httpd
            echo "Ir0nM@n" | sudo -S systemctl status httpd 
        
        Second script
            echo "Am3ric@" | sudo -S yum install httpd -y
            echo "Am3ric@" | sudo -S sed -i 's/^Listen[[:space:]]\+[0-9]\+/Listen 8080/' /etc/httpd/conf/httpd.conf
            cat /etc/httpd/conf/httpd.conf | grep Listen
            echo "Am3ric@" | sudo -S systemctl start httpd
            echo "Am3ric@" | sudo -S systemctl enable httpd
            echo "Am3ric@" | sudo -S systemctl status httpd

        Third script
            echo "BigGr33n" | sudo -S yum install httpd -y
            echo "BigGr33n" | sudo -S sed -i 's/^Listen[[:space:]]\+[0-9]\+/Listen 8080/' /etc/httpd/conf/httpd.conf
            cat /etc/httpd/conf/httpd.conf | grep Listen
            echo "BigGr33n" | sudo -S systemctl start httpd
            echo "BigGr33n" | sudo -S systemctl enable httpd
            echo "BigGr33n" | sudo -S systemctl status httpd

create a Freestyle job
    home page > new Item > name: nautilus-app-deployment > freestyle > select git add repo from gitia > check mark "GitHub hook trigger for GITScm polling"

    Build Steps > Execute shell script on remote host using ssh > add below script
        
        echo "Bl@kW" | sudo -S rm -rf /tmp/web-app
        echo "Bl@kW" | sudo -S git clone -b master http://git.stratos.xfusioncorp.com/sarah/web.git /tmp/web-app
        echo "Bl@kW" | sudo -S rm -rf /var/www/html/*.html
        echo "Bl@kW" | sudo -S cp /tmp/web-app/*.html /var/www/html/
        echo "Bl@kW" | sudo -S chown -R sarah:sarah /var/www/html/
        echo "Bl@kW" | sudo -S rm -rf /tmp/web-app

    on the github/Gitia
        go to repo setting > webhooks > Target: url http://jenkins.stratos.xfusioncorp.com:8080/github-webhook/