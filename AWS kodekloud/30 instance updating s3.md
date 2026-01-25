The Nautilus DevOps team is tasked with enabling internet access for an EC2 instance running in a private subnet. This instance should be able to upload a test file to a public S3 bucket once it can access the internet. To minimize costs, the team has decided to use a NAT Instance instead of a NAT Gateway.

The following components already exist in the environment:
1) A VPC named devops-priv-vpc and a private subnet named devops-priv-subnet have been created.
2) An EC2 instance named devops-priv-ec2 is already running in the private subnet.
3) The EC2 instance is configured with a cron job that uploads a test file to the S3 bucket devops-nat-3535 every minute. Upload will only succeed once internet access is established.

Your task is to:

Create a new public subnet named devops-pub-subnet in the existing VPC.
Launch a NAT Instance in the public subnet using an Amazon Linux 2 AMI and name it devops-nat-instance. Configure this instance to act as a NAT instance. Make sure to use a custom security group for this instance.
After the configuration, verify that the test file devops-test.txt appears in the S3 bucket devops-nat-3535. This indicates successful internet access from the private EC2 instance via the NAT Instance.


####### Solution ######


Open VPC > create internet gateway > attach it to vpc
open vpc > create route table > attach internet-gateway and name route devops-public-rt
open vpc > create subnet:
                    name: devops-pub-subnet
                    availability zone: us-east-1a (same as private subnet availability zone)
                    CIDR ip: 10.1.2.0/24
open vpc > route table > open: devops-public-rt > subnet assocations > Edit subnet associations > select devops-pub-subnet > save

                    
open vpc > attach public-rt to devops-pub-subnet

Open EC2 > launch instance > 
            name: devops-nat-instance
            ami: amazon
            instance type: t2.micro
            vpc: devops-vpc
            subnet: devops-pub-subnet
            Auto-assign-ip: Enable
            security group: 
                source: 0.0.0.0
                destination: anywhere
    launch instance

open ec2 > security group > select private instance security group > attach rule >
                                                                    source: 0.0.0.0
                                                                    destination: custom
                                                                        select: public instance security group

open ec2 > security group > select public instance security group > attach rule >
                                                                    source: 0.0.0.0
                                                                    destination: custom
                                                                        select: private instance security group                                                              

