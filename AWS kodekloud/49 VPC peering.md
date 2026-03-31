The xfusion xfusion team needs to build a secure and scalable log aggregation setup within their AWS environment. The goal is to gather log files from an internal EC2 instance running in a private VPC, transfer them securely to another EC2 instance in a public VPC, and then push those logs to a secure S3 bucket.

1) A VPC named xfusion-priv-vpc already exists with a private subnet named xfusion-priv-subnet, a route table named xfusion-priv-rt, and an EC2 instance named xfusion-priv-ec2 (using ubuntu image). This instance uses the SSH key pair xfusion-key.pem already available on the AWS client host at /root/.ssh/.

2) Your task is to:

Create a new VPC named xfusion-pub-vpc.
Create a subnet named xfusion-pub-subnet and a route table named xfusion-pub-rt under this public VPC.
Attach an internet gateway to xfusion-pub-vpc and configure the public route table to enable internet access.
Launch an EC2 instance named xfusion-pub-ec2 into the public subnet using the same key pair as the private instance.
Create an IAM role named xfusion-s3-role with PutObject permission to an S3 bucket and attach it to the public EC2 instance.
Create a new private S3 bucket named xfusion-s3-logs-6972.
Configure a VPC Peering named xfusion-vpc-peering between the private and public VPCs.
Modify both xfusion-priv-rt and xfusion-pub-rt to route each other's CIDR blocks through the peering connection.
On the private instance, configure a cron job to push the /var/log/boots.log file to the public instance (using scp or rsync).
On the public instance, configure a cron job to push that same file to the created S3 bucket.
The uploaded file must be stored in the S3 bucket under the path xfusion-priv-vpc/boot/boots.log.


### Solution

# Create VPC
 Name: xfusion-pub-vpc
 CIDR: 10.1.0.0/16

# Create two Internet-Gateways one for public vpc and one for private vpc
    1) Name: xfusion-pub-IG -> Attach -> xfusion-pub-vpc
    2) Name: xfusion-private-access -> attach -> xfusion-priv-vpc

# Create 2 public Subnets, one for public vpc and one for private vpc
    1) Name: xfusion-pub-subnet 
       VPC: xfusion-pub-vpc
       CIDR: 10.1.1.0/24
    
    2) Name: public-nat-access
       VPC: xfusion-priv-vpc
       CIDR: 10.10.20.0/24

# Create Nat gateway
  name: give-internet-to-private-subnet
  VPC: xfusion-priv-vpc

# To Verify NAT gateway
####### Wait 2-3 min for nat gatway to spin-up #######

# Update private route table
    - xfusion-priv-rt -> add route -> 0.0.0.0 Nat gatway (give-internet-to-private-subnet) 

# Create Route tables
    1) Name: xfusion-pub-rt
       VPC: xfusion-pub-vpc
       Rules:
            - 0.0.0.0 - internet-gateway (xfusion-pub-IG)

    2) Name: public-nat-for-xfusion
       VPC: xfusion-priv-vpc
       Rules:
            - 0.0.0.0 - internet-gateway (public-nat-access)

# Associate route tables to subnetes
    1) Name: xfusion-pub-rt -> Subnet Associations -> Edit routes -> xfusion-pub-subnet
    2) Name: public-nat-for-xfusion -> Subnet Associations -> Edit routes -> public-nat-access

# Create ec2 instance in this public VPC and subnet 
    - Name: xfusion-pub-ec2
    - Key: xfusion-key
    - VPC: xfusion-pub-vpc
    - subnet: xfusion-pub-subnet
    - Auto-assign public IP: Enable
    - add script 
        #!bin/bash
        sudo apt update
        sudo snap install aws-cli --classic

# create s3 bucket
    Name: xfusion-s3-logs-6972

# create policy
  name: s3Putobject
  json:
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "VisualEditor0",
                "Effect": "Allow",
                "Action": "s3:PutObject",
                "Resource": "arn:aws:s3:::xfusion-s3-logs-24896/*"
            }
        ]
    }


# Create EC2 Role attaching this policy
    name: xfusion-s3-role

# attach this role to EC2
    - ec2 -> xfusion-pub-ec2 -> select -> actions -> security -> Modify Iam role -> xfusion-s3-role -> update

# Create VPC Peering connection
    -> Name: xfusion-vpc-peering
       Requester: xfusion-pub-vpc
       Acceptor: xfusion-priv-vpc
    xfusion-vpc-peering -> Actions -> Accept request

# configure route table of both the vpc to accept the VPC's CIDR 
    - AWS Console -> VPC A -> copy CIDR VPC A (Eg: 10.10.0.0/16)
    -> AWS console -> VPC B -> VPC B subnet -> route table -> 10.10.0.0/16 - vpc peering

    - AWS Console -> VPC B -> copy CIDR VPC B (Eg: 10.1.0.0/16)
    -> AWS console -> VPC A -> VPC A subnet -> route table -> 10.1.0.0/16 - vpc peering

# Copy key to xfusion-pub-ec2 from aws-client
    - scp -i .ssh/xfusion-key.pem .ssh/xfusion-key.pem ubuntu@<public_instance_IP>:/home/ubuntu/xfusion-key.pem

# ssh into xfusion-pub-ec2 from aws-client
    - ssh -i .ssh/xfusion-key.pem ubuntu@<public_instance_IP>
    
    # Copy key to xfusion-priv-ec2 from xfusion-pub-ec2
    - scp -i xfusion-key.pem xfusion-key.pem ubuntu@<PrivateIP>:/home/ubuntu/xfusion-key.pem

    # ssh into xfusion-priv-ec2 from xfusion-pub-ec2
    - ssh -i xfusion-key.pem ubuntu@<PrivateSubnetIP>

# check internet is accessible from private instance
- ping www.google.com 
    # you should see output like this 
        PING www.google.com (142.251.154.119) 56(84) bytes of data.
        64 bytes from 142.251.154.119 (142.251.154.119): icmp_seq=1 ttl=115 time=1.93 ms
        64 bytes from 142.251.154.119 (142.251.154.119): icmp_seq=2 ttl=115 time=1.10 ms
        64 bytes from 142.251.154.119 (142.251.154.119): icmp_seq=3 ttl=115 time=1.09 ms
        64 bytes from 142.251.154.119 (142.251.154.119): icmp_seq=4 ttl=115 time=1.09 ms
        64 bytes from 142.251.154.119 (142.251.154.119): icmp_seq=5 ttl=115 time=1.10 ms

# Create a script in private instance
- nano send_log.sh
#!/bin/bash
SRC="/var/log/boots.log"
DEST="ubuntu@<publicIP>:/home/ubuntu"
KEY="/home/ubuntu/xfusion-key.pem"
scp -i $KEY $SRC $DEST

# make executable script
- chmod +x send_log.sh

# Create CronJob
    - crontab -e  # Open crontab
        - */2 * * * * /home/ubuntu/send_log.sh >> /home/ubuntu/cron.log 2>&1 # Run every 2 minutes

## wait 2 min to verify cronjob ##
# Verify CronJob
    - tail -f /home/ubuntu/cron.log  #Check logs


# Create a script in public instance
- nano send_to_s3.sh
#!/bin/bash
FILE="/home/ubuntu/boots.log"
BUCKET="s3://xfusion-s3-logs-6972/xfusion-priv-vpc/boot/"
aws s3 cp $FILE $BUCKET

# make executable script
- chmod +x send_to_s3.sh

# Create CronJob
    - crontab -e  # Open crontab
        - */2 * * * * /home/ubuntu/send_to_s3.sh >> /home/ubuntu/cron.log 2>&1 # Run every 2 minutes

## wait 2 min to verify cronjob ##
# Verify CronJob
    - tail -f /home/ubuntu/cron.log  #Check logs



