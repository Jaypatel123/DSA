The Nautilus DevOps team needs to implement a Lambda function using a CloudFormation stack. Create a CloudFormation template named /root/nautilus-lambda.yml on the AWS client host and configure it to create the following components. The stack name must be nautilus-lambda-app.

Create a Lambda function named nautilus-lambda.
Use the Runtime Python.
The function should print the body Welcome to KKE AWS Labs!.
Ensure the status code is 200.
Create and use the IAM role named lambda_execution_role.

Use below given AWS Credentials: (You can run the showcreds command on aws-client host to retrieve these credentials)


### solution ###


AWSTemplateFormatVersion: '2010-09-09'
Description: CloudFormation stack to create a basic Lambda function

Resources:
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
        - arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

  NautilusLambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: nautilus-lambda
      Runtime: python3.9
      Handler: index.lambda_handler
      Role: !GetAtt LambdaExecutionRole.Arn
      Timeout: 10
      Code:
        ZipFile: |
          def lambda_handler(event, context):
              return {
                  "statusCode": 200,
                  "body": "Welcome to KKE AWS Labs!"
              }

### Create a Stack using below command
aws cloudformation create-stack \
    --stack-name nautilus-lambda-app \
    --template-body file://nautilus-lambda.yml \
    --capabilities CAPABILITY_NAMED_IAM


### Wait for it to be created

aws cloudformation wait stack-create-complete \
  --stack-name nautilus-lambda-app


### Verification: Invoke the function

aws lambda invoke \
  --function-name nautilus-lambda \
  response.json

Check the output - expected output:

{
  "statusCode": 200,
  "body": "Welcome to KKE AWS Labs!"
}