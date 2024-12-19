import json
import boto3

def lambda_handler(event, context):
    # Initialize Boto3 clients
    s3_client = boto3.client('s3')
    sns_client = boto3.client('sns')
    
    # Replace with your SNS topic ARN
    sns_topic_arn = 'arn:aws:sns:us-east-1:975050024946:Aks-S3-bucket-PublicAccess'
    
    # List all S3 buckets
    response = s3_client.list_buckets()
    buckets = response['Buckets']
    
    pub_access_buckets = []

    # Check each bucket's permission settings
    for bucket in buckets:
        bucket_name = bucket['Name']
        
        # Check the bucket's ACL
        acl = s3_client.get_bucket_acl(Bucket=bucket_name)
        
        # Check permissions
        for grant in acl['Grants']:
            permission = grant['Permission']
            grantee = grant['Grantee']
            
            if grantee['Type'] == 'Group' and 'URI' in grantee:
                access_check = grantee['URI']
                # Check for public read or write permissions
                if (access_check == 'http://acs.amazonaws.com/groups/global/AllUsers' or
                        access_check == 'http://acs.amazonaws.com/groups/global/AuthenticatedUsers'):
                    if permission in ['READ', 'WRITE', 'FULL_CONTROL']:
                        pub_access_buckets.append(bucket_name)
                        
                        # Send notification via SNS
                        sns_client.publish(
                            TopicArn=sns_topic_arn,
                            Message=f'Bucket "{bucket_name}" has public {permission.lower()} permissions.',
                            Subject='Public S3 Bucket Alert'
                        )
                        break
    
    # Print the names of public buckets for logging purposes
    if pub_access_buckets:
        print("Public buckets with read or write permissions:")
        for bucket in pub_access_buckets:
            print(f" - {bucket}")
    else:
        print("No buckets with public read or write permissions found.")