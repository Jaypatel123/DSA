The development team of xFusionCorp Industries is working on to develop a new static website and they are planning to deploy the same on Nautilus App Servers using Jenkins pipeline. They have shared their requirements with the DevOps team and accordingly we need to create a Jenkins pipeline job. Please find below more details about the task:



Click on the Jenkins button on the top bar to access the Jenkins UI. Login using username admin and password Adm!n321.


Similarly, click on the Gitea button on the top bar to access the Gitea UI. Login using username sarah and password Sarah_pass123. There under user sarah you will find a repository named web_app that is already cloned on Storage server under /var/www/html. sarah is a developer who is working on this repository.


Add a slave node named Storage Server. It should be labeled as ststor01 and its remote root directory should be /var/www/html.


We have already cloned repository on Storage Server under /var/www/html.


Apache is already installed on all app Servers its running on port 8080.


Create a Jenkins pipeline job named nautilus-webapp-job (it must not be a Multibranch pipeline) and configure it to:


Deploy the code from web_app repository under /var/www/html on Storage Server, as this location is already mounted to the document root /var/www/html of app servers. The pipeline should have a single stage named Deploy ( which is case sensitive ) to accomplish the deployment.

LB server is already configured. You should be able to see the latest changes you made by clicking on the App button. Please make sure the required content is loading on the main URL https://<LBR-URL> i.e there should not be a sub-directory like https://<LBR-URL>/web_app etc.


Note:


You might need to install some plugins and restart Jenkins service. So, we recommend clicking on Restart Jenkins when installation is complete and no jobs are running on plugin installation/update page i.e update centre. Also, Jenkins UI sometimes gets stuck when Jenkins service restarts in the back end. In this case, please make sure to refresh the UI page.


For these kind of scenarios requiring changes to be done in a web UI, please take screenshots so that you can share it with us for review in case your task is marked incomplete. You may also consider using a screen recording software such as loom.com to record and share your work.


######## solution down ########

install plugins ssh, SSH Credentials, SSH Build Agents, Pipeline

add crediantials natasha

Install Java on natasha storage server and give access to the natasha user and group
    -> sudo yum install java-21-openjdk -y
    -> sudo chown -R natasha:natasha /var/www/html

add known_hosts to the Jenkins master node
    -> ssh into jenkins@jenkins
    -> mkdir -p ~/.ssh
    -> chmod 700 ~/.ssh
    -> touch ~/.ssh/known_hosts
    -> chmod 644 ~/.ssh/known_hosts
        add known_hosts agents natasha (database storage) to jenkins master
            -> ssh jenkins@172.16.238.15 ( Password entering is not required )
            -> yes
    -> cat ~/.ssh/known_hosts -> check known hosts entries 
    
Add agent(Node):
        name: Storage Server
        remote dir: /var/www/html
        label: ststor01
        Launch Method: SSH
        host: ststor01
        credential: natasha/pass
        host key: no verification
    Save

Add Job:
    select pipeline 
        ### Write below script in script section
        pipeline {
            agent { label 'ststor01' }
            stages {
                stage('Deploy') {
                    steps {
                        script {
                            sh '''
                                rm -rf /tmp/web_app
                                git clone http://git.stratos.xfusioncorp.com/sarah/web_app.git /tmp/web_app
                                ls -la /tmp/web_app
                                echo 'Bl@kW' | sudo -S rm -rf /var/www/html/*.html
                                echo 'Bl@kW' | sudo -S cp -r /tmp/web_app/* /var/www/html/
                                rm -rf /tmp/web_app
                            '''
                        }
                    }
                }
            }
        }





