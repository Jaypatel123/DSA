The Nautilus DevOps team is tasked with deploying a containerized application using Amazon's container services. They need to create a private Amazon Elastic Container Registry (ECR) to store their Docker images and use Amazon Elastic Container Service (ECS) to deploy the application. The process involves building a Docker image from a given Dockerfile, pushing it to the ECR, and then setting up an ECS cluster to run the application.

Create a Private ECR Repository:

Create a private ECR repository named datacenter-ecr to store Docker images.
Build and Push Docker Image:

Use the Dockerfile located at /root/pyapp on the aws-client host.
Build a Docker image using this Dockerfile.
Tag the image with latest tag.
Push the Docker image to the datacenter-ecr repository.
Create and Configure ECS cluster:

Create an ECS cluster named datacenter-cluster using the Fargate launch type.
Create an ECS Task Definition:

Define a task named datacenter-taskdefinition using the Docker image from the datacenter-ecr ECR repository.
Specify necessary CPU and memory resources.
Deploy the Application Using ECS Service:

Create a service named datacenter-service on the datacenter-cluster to run the task.
Ensure the service runs at least one task.

Use below given AWS Credentials: (You can run the showcreds command on aws-client host to retrieve these credentials)


### solution

# check aws exists or not
    aws --version
# check for images
    docker images
#   docker build local 
    cd pyapp
    docker build -t 113749894636.dkr.ecr.us-east-1.amazonaws.com/datacenter-ecr:latest .
# before pushing to ECR, register
    aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 113749894636.dkr.ecr.us-east-1.amazonaws.com

# check ecr registration
   cat ~/.docker/config.json
# push it to docker
   docker push 113749894636.dkr.ecr.us-east-1.amazonaws.com/datacenter-ecr:latest

# AWS console -> ECS -> create cluster -> create taskdefinition and attach image -> create service inside created ECS cluster

# wait for 3-5 min until deployment is ready