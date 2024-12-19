import boto3
import datetime

def lambda_handler(event, context):
    # Initialize a boto3 S3 client
    s3_client = boto3.client('s3')

    # Specify the bucket name 
    bucket_name = 'akshaybucket32' 
    # Get the current date and time 
    current_time = datetime.datetime.now(datetime.timezone.utc) 
    
    # List objects in the specified bucket 
    response = s3_client.list_objects_v2(Bucket=bucket_name) 
    
    if 'Contents' not in response:
        print("Bucket is empty or does not exist.")

    #print(f"Contents in a bucket mentioned looks like this: {response}")

    objects = response['Contents'] 
    #print(f"objects in bucket {bucket_name} is: {objects}")
    
    deleted_objects = [] 
    
    # Check each object to see if it is older than 30 days and delete it 
    
    for obj in objects:
        print(f"each object in objects as in obj looks like this: {obj}")
        obj_key = obj['Key'] 
        obj_last_modified = obj['LastModified'] 
        
        # Calculate the object's age 
        object_age = (current_time - obj_last_modified).days 
        if object_age > 30: # Delete the object 
            s3_client.delete_object(Bucket=bucket_name, Key=obj_key) 
            deleted_objects.append(obj_key) 
            print(f"Deleted object: {obj_key}") # Print the names of deleted objects 
        
    if deleted_objects: 
        print("Deleted objects older than 30 days:") 
        for obj in deleted_objects: 
            print(f" - {obj}")     