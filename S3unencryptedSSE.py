import boto3

def lambda_handler(event, context):
    # Initialize a boto3 S3 client
    s3_client = boto3.client('s3')

    # List all S3 buckets
    response = s3_client.list_buckets()
    buckets = response['Buckets']

    unencrypted_buckets = []

    # Check each bucket for server-side encryption
    for bucket in buckets:
        bucket_name = bucket['Name']
        
        encryption = s3_client.get_bucket_encryption(Bucket=bucket_name)
        encryption_bucket = encryption['ServerSideEncryptionConfiguration']['Rules']
        print(f"Bucket '{bucket_name}' has encryption: {encryption_bucket}")

    # Print names of unencrypted buckets for logging purposes
    if unencrypted_buckets:
        print("Unencrypted buckets:")
        for bucket in unencrypted_buckets:
            print(f" - {bucket}")
    else:
        print("All buckets are encrypted.")