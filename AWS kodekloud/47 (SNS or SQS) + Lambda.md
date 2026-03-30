The Nautilus DevOps team needs to implement priority queuing using Amazon SQS and SNS. The goal is to create a system where messages with different priorities are handled accordingly. You are required to use AWS CloudFormation to deploy the necessary resources in your AWS account. The CloudFormation template should be created on the AWS client host at /root/datacenter-priority-stack.yml, the stack name must be datacenter-priority-stack and it should create the following resources:

Two SQS queues named datacenter-High-Priority-Queue and datacenter-Low-Priority-Queue.
An SNS topic named datacenter-Priority-Queues-Topic.
A Lambda function named datacenter-priorities-queue-function that will consume messages from the SQS queues. The Lambda function code is provided in /root/index.py on the AWS client host.
An IAM role named lambda_execution_role that provides the necessary permissions for the Lambda function to interact with SQS and SNS.
Once the stack is deployed, to test the same you can publish messages to the SNS topic, invoke the Lambda function and observe the order in which they are processed by the Lambda function. The high-priority message must be processed first.

topicarn=$(aws sns list-topics --query "Topics[?contains(TopicArn, 'datacenter-Priority-Queues-Topic')].TopicArn" --output text)

aws sns publish --topic-arn $topicarn --message 'High Priority message 1' --message-attributes '{"priority" : { "DataType":"String", "StringValue":"high"}}'

aws sns publish --topic-arn $topicarn --message 'High Priority message 2' --message-attributes '{"priority" : { "DataType":"String", "StringValue":"high"}}'

aws sns publish --topic-arn $topicarn --message 'Low Priority message 1' --message-attributes '{"priority" : { "DataType":"String", "StringValue":"low"}}'

aws sns publish --topic-arn $topicarn --message 'Low Priority message 2' --message-attributes '{"priority" : { "DataType":"String", "StringValue":"low"}}'


Use below given AWS Credentials: (You can run the showcreds command on aws-client host to retrieve these credentials)


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
  
  SNSDatacenterTopic:
    Type: AWS::SNS::Topic
    Properties:
      TopicName: datacenter-Priority-Queues-Topic

  SQSHighPriorityQueue:
    Type: AWS::SQS::Queue
    Properties:
      QueueName: datacenter-High-Priority-Queue
      VisibilityTimeout: 30
  
  SQSLowPriorityQueue:
    Type: AWS::SQS::Queue
    Properties:
      QueueName: datacenter-Low-Priority-Queue
      VisibilityTimeout: 30
  
  SNSHighSubscription:
    Type: AWS::SNS:Subscription
    Properties:
      TopicArn: !Ref SNSDatacenterTopic
      Endpoint: !GetAtt SQSHighPriorityQueue.Arn
      Protocol: sqs
      RawMessageDelievery: true
      FilterPolicy: {"priority": ["High"]}
  
  SNSLowSubscription:
    Type: AWS:SNS:Subscription
    Properties:
      TopicArn: !Ref SNSDatacenterTopic
      Endpoint: !GetAtt SQSLowPriorityQueue.Arn
      Protocol: sqs
      RawMessageDelievery: true
      FilterPolicy: {"priority": ["High"]}
  
  SQSHighQueuePolicy:
    Type: AWS:SQS:QueuePolicy
    Properties:
      Queues:
        - !Ref SQSHighPriorityQueue
      PolicyDocument:
        Id: AllowIncomingMessageFromSNS
        Statement:
          - Effect: Allow
            Principal: '*'
            Action: 
              - sqs.sendMessage
            Resource:
              - !GetAtt SQSHighPriorityQueue.Arn
            Condition:
              ArnEquals:
                aws:SourceArn: !Ref SNSDatacenterTopic
    
  SQSLowQueuePolicy:
    Type: AWS:SQS:QueuePolicy
    Properties:
      Queues: 
        - !Ref SQSLowPriorityQueue
      PolicyDocument:
        Id: AllowIncomingMessageFromSNS
        Statement:
          - Effect: Allow
            Principal: '*'
            Action: 
              - sqs.sendMessage
            Resource:
              - !GetAtt SQSLowPriorityQueue.Arn
            Condition:
              ArnEquals:
                aws:SourceArn: !Ref SNSDatacenterTopic

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
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/AmazonSQSFullAccess
      Path: /


  MyLambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: datacenter-priorities-queue-function
      Runtime: python3.9
      Handler: index.lambda_handler
      Role: !GetAtt LambdaExecutionRole.Arn
      Code:
        ZipFile: >
          import boto3
          import os
          sqs = boto3.client('sqs')
          def delete_message(queue_url, receipt_handle, message):
              response = sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
              return "Message " + "'" + message + "'" + " deleted"
              
          def poll_messages(queue_url):
              QueueUrl=queue_url
              response = sqs.receive_message(
                  QueueUrl=QueueUrl,
                  AttributeNames=[],
                  MaxNumberOfMessages=1,
                  MessageAttributeNames=['All'],
                  WaitTimeSeconds=3
              )
              if "Messages" in response:
                  receipt_handle=response['Messages'][0]['ReceiptHandle']
                  message = response['Messages'][0]['Body']
                  delete_response = delete_message(QueueUrl,receipt_handle,message)
                  return delete_response
              else:
                  return "No more messages to poll"
          def lambda_handler(event, context):
              response = poll_messages(os.environ['high_priority_queue'])
              if response == "No more messages to poll":
                  response = poll_messages(os.environ['low_priority_queue'])
              return response
      Timeout: 10
      MemorySize: 128
      Environment:
        Variables:
          high_priority_queue: !Ref SQSHighPriorityQueue
          low_priority_queue: !Ref SQSLowPriorityQueue
      
  HighPriorityEventsource:
    Type: AWS::Lambda::EventSourceMapping
    Properties:
      EventSourceArn: !GetAtt SQSHighPriorityQueue.Arn
      FunctionName: !Ref LambdaFunction
      BatchSiza: 1
      Enabled: true


## Run Lambda Function
aws cloudformation create-stack \
    --stack-name datacenter-priority-stack \
    --template-body file://datacenter-priority-stack.yml \
    --capabilities CAPABILITY_NAMED_IAM