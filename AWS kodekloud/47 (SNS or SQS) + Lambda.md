The devops devops team needs to implement priority queuing using Amazon SQS and SNS. The goal is to create a system where messages with different priorities are handled accordingly. You are required to use AWS CloudFormation to deploy the necessary resources in your AWS account. The CloudFormation template should be created on the AWS client host at /root/devops-priority-stack.yml, the stack name must be devops-priority-stack and it should create the following resources:

Two SQS queues named devops-High-Priority-Queue and devops-Low-Priority-Queue.
An SNS topic named devops-Priority-Queues-Topic.
A Lambda function named devops-priorities-queue-function that will consume messages from the SQS queues. The Lambda function code is provided in /root/index.py on the AWS client host.
An IAM role named lambda_execution_role that provides the necessary permissions for the Lambda function to interact with SQS and SNS.
Once the stack is deployed, to test the same you can publish messages to the SNS topic, invoke the Lambda function and observe the order in which they are processed by the Lambda function. The high-priority message must be processed first.

topicarn=$(aws sns list-topics --query "Topics[?contains(TopicArn, 'devops-Priority-Queues-Topic')].TopicArn" --output text)

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

# vi devops-priority-stack.yml
AWSTemplateFormatVersion: '2010-09-09'
Description: SQS priority queues template

Resources:
  SQSHighPriorityQueue:
    Type: AWS::SQS::Queue
    Properties:
      VisibilityTimeout: 180
      QueueName: devops-High-Priority-Queue

  SQSLowPriorityQueue:
    Type: AWS::SQS::Queue
    Properties:
      VisibilityTimeout: 180
      QueueName: devops-Low-Priority-Queue

  PriorityQueuesTopic:
    Type: AWS::SNS::Topic
    Properties: 
      TopicName: devops-Priority-Queues-Topic 

  SQSHighQueuePolicy:
    Type: AWS::SQS::QueuePolicy
    Properties:
      Queues:
        - !Ref SQSHighPriorityQueue
      PolicyDocument:
        Id: AllowIncomingMessageFromSNS
        Statement:
          -
            Effect: Allow
            Principal: '*'
            Action:
              - sqs:SendMessage
            Resource:
              - !GetAtt SQSHighPriorityQueue.Arn
            Condition:
              ArnEquals:
                aws:SourceArn: !Ref PriorityQueuesTopic

  SQSLowQueuePolicy:
    Type: AWS::SQS::QueuePolicy
    Properties:
      Queues:
        - !Ref SQSLowPriorityQueue
      PolicyDocument:
        Id: AllowIncomingMessageFromSNS
        Statement:
          -
            Effect: Allow
            Principal: '*'
            Action:
              - sqs:SendMessage
            Resource:
              - !GetAtt SQSLowPriorityQueue.Arn
            Condition:
              ArnEquals:
                aws:SourceArn: !Ref PriorityQueuesTopic

  SNSHighSubscription:
    Type: AWS::SNS::Subscription
    Properties:
      TopicArn: !Ref PriorityQueuesTopic
      Endpoint: !GetAtt SQSHighPriorityQueue.Arn
      Protocol: sqs
      RawMessageDelivery: true
      FilterPolicy: {"priority": ["high"]}

  SNSLowSubscription:
    Type: AWS::SNS::Subscription
    Properties:
      TopicArn: !Ref PriorityQueuesTopic
      Endpoint: !GetAtt SQSLowPriorityQueue.Arn
      Protocol: sqs
      RawMessageDelivery: true
      FilterPolicy: {"priority": ["low"]}

  LambdaRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: lambda_execution_role
      AssumeRolePolicyDocument:
        Statement:
          - Action:
            - sts:AssumeRole
            Effect: Allow
            Principal:
              Service:
              - lambda.amazonaws.com
        Version: 2012-10-17
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/AmazonSQSFullAccess
      Path: /

  LambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: devops-priorities-queue-function
      Description: Priority queue function
      Runtime: python3.9
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

      Handler: index.lambda_handler
      MemorySize: 128
      Timeout: 10
      Role:
        Fn::GetAtt:
          - LambdaRole
          - Arn
      Environment:
        Variables:
          high_priority_queue: !Ref SQSHighPriorityQueue
          low_priority_queue: !Ref SQSLowPriorityQueue

  HighPriorityEventSource:
    Type: AWS::Lambda::EventSourceMapping
    Properties:
      EventSourceArn: !GetAtt SQSHighPriorityQueue.Arn
      FunctionName: !Ref LambdaFunction
      BatchSize: 1
      Enabled: true

Outputs:
  SNSTopicARN:
    Value: !Ref PriorityQueuesTopic

## Create CloudFormation Stack
aws cloudformation create-stack \
    --stack-name devops-priority-stack \
    --template-body file://devops-priority-stack.yml \
    --capabilities CAPABILITY_NAMED_IAM

## check Stack is getting created or it's failing

aws cloudformation wait stack-create-complete \
  --stack-name devops-priority-stack 


Test it by running the commands provided in the task description
