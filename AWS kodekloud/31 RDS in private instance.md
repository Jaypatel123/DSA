As a member of the Nautilus DevOps Team, your task is to perform the following:

Provision a Private RDS Instance: Create a new private RDS instance named xfusion-rds using a sandbox template, further it must be a db.t3.micro type instance.
Engine Configuration: Use the MySQL engine with version 8.4.x.
Enable Storage Autoscaling: Enable storage autoscaling and set the threshold value to 50GB. Keep the rest of the configurations as default.
Instance Availability: Ensure the instance is in the available state before submitting this task.


##### solution 

Step 1: Open RDS

Log in to AWS Management Console

Search → RDS

Click Databases

Click Create database

Step 2: Database Creation Method

Creation method: ✅ Standard create

Step 3: Engine Configuration

Engine type: ✅ MySQL

Engine version: ✅ MySQL 8.4.x
(Example: 8.4.0 – choose the latest 8.4.x available)

⚠️ Make sure it explicitly shows 8.4.x, not 8.0.x.

Step 4: Templates

Template: ✅ Sandbox / Dev-Test

Step 5: DB Settings
Setting	Value
DB instance identifier	nautilus-rds
Master username	admin
Master password	Set (or auto-generate)
Step 6: Instance Configuration

DB instance class

Category: Burstable classes (t class)

Type: ✅ db.t3.micro

Step 7: Storage (IMPORTANT)
Setting	Value
Storage type	General Purpose (gp3 or default)
Allocated storage	Default (20 GB)
Enable storage autoscaling	✅ Yes
Maximum storage threshold	✅ 50 GB

⚠️ This is the autoscaling limit, not initial storage.

Step 8: Connectivity (PRIVATE RDS)
Setting	Value
VPC	Default or your custom VPC
DB subnet group	Private subnet group
Public access	❌ No
VPC security group	Default or private SG

✅ This guarantees no public IP

Step 9: Database Authentication

Database authentication: Password authentication (default)

(Keep defaults as instructed)

Step 10: Additional Configuration

Expand Additional configuration and keep defaults, except:

Setting	Value
Initial database name	nautilusdb (optional)
Backup retention	Default
Encryption	Default
Deletion protection	Default
Step 11: Create Database

Click Create database

⏳ Creation time: 5–10 minutes

Step 12: Verify Instance Availability (MANDATORY)

Go to RDS → Databases

Select nautilus-rds

Confirm:

Status: ✅ Available

Publicly accessible: ❌ No

Engine version: MySQL 8.4.x

Instance class: db.t3.micro

Storage autoscaling: Enabled (Max 50 GB)

✅ Only submit once the status shows Available