import json
import boto3


def lambda_handler(event, context):
    sns_client = boto3.client('sns')
    ec2_client = boto3.client('ec2')
    
    # Extract instance details from the event
    detail = event['detail']
    instance_id = detail['instance-id']
    state = detail['state']
    
    # Fetch instance details (optional, for more information)
    instance_info = ec2_client.describe_instances(InstanceIds=[instance_id])
    instance_details = instance_info['Reservations'][0]['Instances'][0]
    
    # Prepare the SNS message
    message = {
        'InstanceId': instance_id,
        'State': state,
        'InstanceType': instance_details['InstanceType'],
        'LaunchTime': instance_details['LaunchTime'].strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Publish the message to SNS
    sns_client.publish(
        TopicArn='arn:aws:sns:us-east-1:975050024946:Aks-Monitor-EC2-InstanceStates',  # Replace with your SNS topic ARN
        Message=json.dumps(message),
        Subject=f'EC2 Instance State Change: {instance_id}'
    )