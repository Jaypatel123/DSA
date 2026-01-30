The DevOps team was looking for a solution where they want to restart Apache service on all app servers if the deployment goes fine on these servers in Stratos Datacenter. After having a discussion, they came up with a solution to use Jenkins chained builds so that they can use a downstream job for services which should only be triggered by the deployment job. So as per the requirements mentioned below configure the required Jenkins jobs.



Click on the Jenkins button on the top bar to access the Jenkins UI. Login using username admin and Adm!n321 password.


Similarly you can access Gitea UI on port 8090 and username and password for Git is sarah and Sarah_pass123 respectively. Under user sarah you will find a repository named web.


Apache is already installed and configured on all app server so no changes are needed there. The doc root /var/www/html on all these app servers is shared among the Storage server under /var/www/html directory.


1. Create a Jenkins job named nautilus-app-deployment and configure it to pull change from the master branch of web repository on Storage server under /var/www/html directory, which is already a local git repository tracking the origin web repository. Since /var/www/html on Storage server is a shared volume so changes should auto reflect on all apps.


2. Create another Jenkins job named manage-services and make it a downstream job for nautilus-app-deployment job. Things to take care about this job are:


a. This job should restart httpd service on all app servers.

b. Trigger this job only if the upstream job i.e nautilus-app-deployment is stable.


LB server is already configured. Click on the App button on the top bar to access the app. You should be able to see the latest changes you made. Please make sure the required content is loading on the main URL https://<LBR-URL> i.e there should not be a sub-directory like https://<LBR-URL>/web etc.


Note:


1. You might need to install some plugins and restart Jenkins service. So, we recommend clicking on Restart Jenkins when installation is complete and no jobs are running on plugin installation/update page i.e update centre. Also some times Jenkins UI gets stuck when Jenkins service restarts in the back end so in such case please make sure to refresh the UI page.


2. Make sure Jenkins job passes even on repetitive runs as validation may try to build the job multiple times.


3. Deployment related tasks should be done by sudo user on the destination server to avoid any permission issues so make sure to configure your Jenkins job accordingly.


4. For these kind of scenarios requiring changes to be done in a web UI, please take screenshots so that you can share it with us for review in case your task is marked incomplete. You may also consider using a screen recording software such as loom.com to record and share your work.

### solution ###

Update plugins and restart jenkins

Install following plugins: Git, SSH, ssh credentials

Add credentials for all 3 app server

Add SSH Server:
Goto Manage Jenkins > System > SSH Remote server > Add Servers

Create primary deployment JOb:
    Job Name: nautilus-app-deployment
    Type: Freestyle Project
    SCM: GIT

    Add Repository URL
    Build Steps:
        Shell Execute, and add this line:
            sshpass -p "Bl@kW" scp -r -o StrictHostKeyChecking=no ./* natasha@ststor01:/var/www/html

Create Another Job: manage-services
    job name: manage-services
    Triggers > Build after other projects are built > add: nautilus-app-deployment > select: Trigger only if build is stable
    Build Steps: create 3 build steps of Execute shell script on remote host using ssh

    For each build step, select each app servers and execution command:
    echo 'app-server-password' | sudo -S systemctl restart httpd
    Goto nautilus-app-deployment job and add post build action:



Now build nautilus-app-deployment job, once it build successfully manage-services will start building automatically.

Reload app link








###### Not working solution, tried pipeline method



plugins download: Gitea, Pipeline, SSH, ssh credentials

add Gitea server in systems

create token

Gitea login and attaching URL
token_url = https://admin:11465db752d04a74402e6576eb4c75ca7b@8080-port-gflfnb4djgle7ybt.labs.kodekloud.com/job/nautilus-app-deployment/build?token=jay123


Jenkins pipeline:

pipeline {
    agent any
    stages {
        stage('Deploy'){
            steps {
                script {
                    sh '''
                        sshpass -p "Bl@kW" ssh -o StrictHostKeyChecking=no natasha@ststor01 bash -c "'
                            echo "Bl@kW" | sudo -S rm -rf /tmp/web
                            echo "Bl@kW" | sudo -S git clone -b master http://git.stratos.xfusioncorp.com/sarah/web.git /tmp/web
                            echo "Bl@kW" | sudo -S chown -R natasha:natasha /var/www/html
                            echo "Bl@kW" | sudo -S rm -rf /var/www/html/*.html
                            echo "Bl@kW" | sudo -S cp /tmp/web/*.html /var/www/html/
                            ls -al /tmp/web/
                        '"
                    '''
                }
            }
        }
        stage('restart tony') {
            steps {
                script {
                    sh '''
                        sshpass -p "Ir0nM@n" ssh -o StrictHostKeyChecking=no tony@stapp01 bash -c "'
                            echo "Ir0nM@n" | sudo -S systemctl restart httpd
                            echo "Ir0nM@n" | sudo -S systemctl enable httpd
                        '"
                    '''
                }
            }    
        }
        stage('restart steve') {
            steps {
                script {
                    sh '''
                        sshpass -p "Am3ric@" ssh -o StrictHostKeyChecking=no steve@stapp02 bash -c "'
                            echo "Am3ric@" | sudo -S systemctl restart httpd
                            echo "Am3ric@" | sudo -S systemctl enable httpd
                        '"
                    '''
                }
            }
        }
        stage('restart banner') {
            steps {
                script {
                    sh '''
                        sshpass -p "BigGr33n" ssh -o StrictHostKeyChecking=no banner@stapp03 bash -c "'
                            echo "BigGr33n" | sudo -S systemctl restart httpd
                            echo "BigGr33n" | sudo -S systemctl enable httpd
                        '"
                    '''
                }
            }
        }
    }
}