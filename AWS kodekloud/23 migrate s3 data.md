As part of a data migration project, the team lead has tasked the team with migrating data from an existing S3 bucket to a new S3 bucket. The existing bucket contains a substantial amount of data that must be accurately transferred to the new bucket. The team is responsible for creating the new S3 bucket and ensuring that all data from the existing bucket is copied or synced to the new bucket completely and accurately. It is imperative to perform thorough verification steps to confirm that all data has been successfully transferred to the new bucket without any loss or corruption.

As a member of the Nautilus DevOps Team, your task is to perform the following:

Create a New Private S3 Bucket: Name the bucket nautilus-sync-19143.

Data Migration: Migrate the entire data from the existing nautilus-s3-17637 bucket to the new nautilus-sync-19143 bucket.

Ensure Data Consistency: Ensure that both buckets have the same data.

Use AWS CLI: Use the AWS CLI to perform the creation and data migration tasks.



Notes:

Create the resources only in us-east-1 region.
To display or hide the terminal of the AWS client machine, you can use the expand toggle button as shown below:\n


## solution ##

aws s3api create-bucket --bucket newbucketname

aws s3 sync s3://source-bucket s3://destination-bucket(new_bucket) --dryrun

aws s3 sync s3://source-bucket s3://destination-bucket(new_bucket)