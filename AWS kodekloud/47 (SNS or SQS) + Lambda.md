The Nautilus DevOps team needs to implement priority queuing using Amazon SQS and SNS. The goal is to create a system where messages with different priorities are handled accordingly. You are required to use AWS CloudFormation to deploy the necessary resources in your AWS account. The CloudFormation template should be created on the AWS client host at /root/nautilus-priority-stack.yml, the stack name must be nautilus-priority-stack and it should create the following resources:

Two SQS queues named nautilus-High-Priority-Queue and nautilus-Low-Priority-Queue.
An SNS topic named nautilus-Priority-Queues-Topic.
A Lambda function named nautilus-priorities-queue-function that will consume messages from the SQS queues. The Lambda function code is provided in /root/index.py on the AWS client host.
An IAM role named lambda_execution_role that provides the necessary permissions for the Lambda function to interact with SQS and SNS.
Once the stack is deployed, to test the same you can publish messages to the SNS topic, invoke the Lambda function and observe the order in which they are processed by the Lambda function. The high-priority message must be processed first.

topicarn=$(aws sns list-topics --query "Topics[?contains(TopicArn, 'nautilus-Priority-Queues-Topic')].TopicArn" --output text)

aws sns publish --topic-arn $topicarn --message 'High Priority message 1' --message-attributes '{"priority" : { "DataType":"String", "StringValue":"high"}}'

aws sns publish --topic-arn $topicarn --message 'High Priority message 2' --message-attributes '{"priority" : { "DataType":"String", "StringValue":"high"}}'

aws sns publish --topic-arn $topicarn --message 'Low Priority message 1' --message-attributes '{"priority" : { "DataType":"String", "StringValue":"low"}}'

aws sns publish --topic-arn $topicarn --message 'Low


### Solution

# Go to AWS Console 
    - Create S3 bucket
        - name:  hellolambdafunction-123

# Create index.py into zip format

zip index.zip index.py

# Push lambda function to this s3 bucket
aws s3 cp index.zip s3://hellolambdafunction-123/

# vi nautilus-priority-stack.yml
AWSTemplateFormatVersion: '2010-09-09'
Description: CloudFormation template to create an SQS Queue

Resources:
  MyQueue:
    Type: AWS::SQS::Queue
    Properties:
      QueueName: xfusion-High-Priority-Queue
      VisibilityTimeout: 30
      DelaySeconds: 0
      MessageRetentionPeriod: 345600
      ReceiveMessageWaitTimeSeconds: 0
  MyQueue:
    Type: AWS::SQS::Queue
    Properties:
      QueueName: xfusion-Low-Priority-Queue
      VisibilityTimeout: 30
      DelaySeconds: 0
      MessageRetentionPeriod: 345600
      ReceiveMessageWaitTimeSeconds: 0
  
  LambdaExecutionRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: lambda_execution_role
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: sts:AssumeRole
  
  MyIAMPolicy:
    Type: AWS::IAM::Policy
    Properties:
      PolicyName: SQS&SNSPolicy
      Roles:
        - !Ref lambda_execution_role
      PolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Action: 
              - sqs:ReceiveMessage
              - sqs:DeleteMessage
              - sqs:GetQueueAttributes
              - sqs:GetQueueUrl
              - sqs:ChangeMessageVisibility
            Resource:
              - arn:aws:sqs:us-east-1:766182622417:datacenter-High-Priority-Queue
              - arn:aws:sqs:us-east-1:766182622417:datacenter-Low-Priority-Queue
          - Effect: Allow
            Action: 
              - s3:GetObject
            Resource:
              - arn:aws:s3:::hellolambdafunction-123
              - arn:aws:s3:::hellolambdafunction-123/*
          - Effect: Allow
            Action: 
              - sns:Publish
              - sns:Subscribe
              - sns:ListSubscriptions
              - sns:ListTopics
            Resource: arn:aws:sns:us-east-1:534953745331:datacenter-Priority-Queues-Topic


  MyLambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: xfusion-priorities-queue-function
      Runtime: python3.12
      Handler: index.lambda_handler
      Role: !GetAtt LambdaExecutionRole.Arn
      Code:
        S3Bucket: hellolambdafunction-123
        S3Key: index.zip
      Timeout: 10
      MemorySize: 128

  MySNSTopic:
    Type: AWS::SNS::Topic
    Properties:
      TopicName: xfusion-Priority-Queues-Topic
  
  LambdaInvokePermission:
    Type: AWS::Lambda::Permission
    Properties:
      FunctionName: !Ref xfusion-priorities-queue-function
      Action: lambda:InvokeFunction
      Principal: sns.amazonaws.com
      SourceArn: !Ref MySNSTopic
  
  SNSToLambdaSubscription:
    Type: AWS::SNS::Subscription
    Properties:
      Protocol: lambda
      TopicArn: !Ref MySNSTopic
      Endpoint: !GetAtt MyLambdaFunction.Arn
  
Outputs:
  SNSTopicARN:
    Description: ARN of the SNS topic
    Value: !Ref MySNSTopic

  LambdaFunctionARN:
    Description: ARN of the Lambda function
    Value: !GetAtt MyLambdaFunction.Arn


## Run Lambda Function
aws cloudformation create-stack \
    --stack-name xfusion-priority-stack \
    --template-body file://xfusion-priority-stack.yml \
    --capabilities CAPABILITY_NAMED_IAM