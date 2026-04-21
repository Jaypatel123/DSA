The Nautilus DevOps Team has recently been informed by the Development Team that their EC2 instance is running out of storage space. This instance, crucial for development activities, is named devops-ec2 and currently has an attached volume of 8 GiB. To accommodate the increasing data requirements, the storage needs to be expanded to 12 GiB. This change should ensure that the expanded space is immediately available for use within the instance without disrupting ongoing activities.

Identify Volume: Find the volume attached to the devops-ec2 instance.

Expand Volume: Increase the volume size from 8 GiB to 12 GiB.

Reflect Changes: Ensure the root (/) partition within the instance reflects the expanded size from 8 GiB to 12 GiB.

SSH Access: Use the key pair located at /root/devops-keypair.pem on the aws-client host to SSH into the EC2 instance.



AWS Credentials: (You can run the showcreds command on aws-client host to retrieve these credentials)

### SOlution

Ec2 -> devops-ec2 -> Storage -> click on "volume ID" 

Volume -> select -> action -> modify volume -> update 8 -> 12 -> save

# open aws-client
ssh -i devops-keypair.pem ec2-user@<public-IP>

sudo su -

# Check if OS detects new disk size
lsblk

# Check filesystem size (IMPORTANT)
df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/xvda1       8G   2G    6G   25% /

👉 If this still shows 8G, your filesystem is NOT expanded yet.

# Expand partition
# For most modern EC2 (Amazon Linux / Ubuntu):
    sudo growpart /dev/xvda 1
# OR (NVMe-based instances):
    sudo growpart /dev/nvme0n1 1

# Expand filesystem
If using XFS (Amazon Linux 2 default):
command: sudo xfs_growfs -d /

# Verify Again
df -h

Filesystem      Size  Used Avail Use% Mounted on
/dev/xvda1      12G   ...