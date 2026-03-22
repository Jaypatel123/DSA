The Nautilus DevOps team is expanding their AWS infrastructure and requires the setup of a private Virtual Private Cloud (VPC) along with a subnet. This VPC and subnet configuration will ensure that resources deployed within them remain isolated from external networks and can only communicate within the VPC. Additionally, the team needs to provision an EC2 instance under the newly created private VPC. This instance should be accessible only from within the VPC, allowing for secure communication and resource management within the AWS environment.

Create a VPC named xfusion-priv-vpc with the CIDR block 10.0.0.0/16.

Create a subnet named xfusion-priv-subnet inside the VPC with the CIDR block 10.0.1.0/24 and auto-assign IP option must not be enabled.

Create an EC2 instance named xfusion-priv-ec2 inside the subnet and instance type must be t2.micro.

Ensure the security group of the EC2 instance allows access only from within the VPC's CIDR block.

Create the main.tf file (do not create a separate .tf file) to provision the VPC, subnet and EC2 instance.

Use variables.tf file with the following variable names:

KKE_VPC_CIDR for the VPC CIDR block.
KKE_SUBNET_CIDR for the subnet CIDR block.
Use the outputs.tf file with the following variable names:

KKE_vpc_name for the name of the VPC.
KKE_subnet_name for the name of the subnet.
KKE_ec2_private for the name of the EC2 instance.

Notes:

The Terraform working directory is /home/bob/terraform.

Right-click under the EXPLORER section in VS Code and select Open in Integrated Terminal to launch the terminal.

Before submitting the task, ensure that terraform plan returns No changes. Your infrastructure matches the configuration.


### solution 

# variables.tf
variable "vpc_name" {
    default = "xfusion-priv-vpc"
}

variable "KKE_VPC_CIDR" {
    default = "10.0.0.0/16"
}

variable "priv_sub_name" {
    default = "xfusion-priv-subnet"
}

variable "KKE_SUBNET_CIDR" {
    default = "10.0.1.0/24"
}

variable "instance_name" {
    default = "xfusion-priv-ec2"
}


# output.tf
output "KKE_vpc_name" {
    value = aws_vpc.vpc.tags["Name"]
}

output "KKE_subnet_name" {
    value = aws_subnet.private_subnet.tags["Name"]
}

output "KKE_ec2_private" {
    value = aws_instance.private_instance.tags["Name"]
}

# main.tf
resource "aws_vpc" "vpc" {
    cidr_block = var.KKE_VPC_CIDR
    tags = {
        Name = var.vpc_name
    }
}

resource "aws_subnet" "private_subnet" {
    vpc_id = aws_vpc.vpc.id
    cidr_block = var.KKE_SUBNET_CIDR

    tags = {
        Name = var.priv_sub_name
    }
}

resource "aws_security_group" "private_security_group" {
    name = "secure_private_instance"
    description = "this security_group is going to secure private instance"
    vpc_id = aws_vpc.vpc.id

    ingress {
        description = "created to allow traffic from subnet cidr"
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = [aws_subnet.private_subnet.cidr_block]
    }
}

resource "aws_instance" "private_instance" {
    ami = "ami-0c101f26f147fa7fd"
    subnet_id = aws_subnet.private_subnet.id
    instance_type = "t2.micro"
    vpc_security_group_ids = [aws_security_group.private_security_group.id]
    associate_public_ip_address = false
    tags = {
        Name = var.instance_name
    }
}

