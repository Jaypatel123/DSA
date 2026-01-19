The Nautilus DevOps team needs to set up a new EC2 instance that can be accessed securely from their landing host (aws-client). The instance should be of type t2.micro and named datacenter-ec2. A new SSH key should be created on the aws-client host under the/root/.ssh/ folder, if it doesn't already exist. This key should then be added to the root user's authorised keys on the EC2 instance, allowing passwordless SSH access from the aws-client host.


Use below given AWS Credentials: (You can run the showcreds command on aws-client host to retrieve these credentials)

Console URL	https://403751978661.signin.aws.amazon.com/console?region=us-east-1
Username	kk_labs_user_586984
Password	HauS%7!L%!GM
Start Time	Mon Jan 19 18:13:20 UTC 2026
End Time	Mon Jan 19 19:13:20 UTC 2026

Notes:

Create the resources only in us-east-1 region.

To display or hide the terminal of the AWS client machine, you can use the expand toggle button as shown below:

#### Solution ####

# create a key
from kodekloud console > run command
    > cd .ssh
    > ssh-keygen -t ed25519 -C "your-email.com"
    > cat id_ed25519.pub
    copy entire key

create a instance using a key-pair > from your local machine terminal log into instance > run command
    > sudo su -
    > cd .ssh/
    > vi authorized_keys
    paste the key in the next line
    save
    



