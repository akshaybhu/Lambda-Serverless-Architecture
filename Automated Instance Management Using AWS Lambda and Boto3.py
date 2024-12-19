import os
import boto3

ec2 = boto3.resource("ec2", region_name="us-east-1")

def lambda_handler(event, context):

    # Iterate through all instances in us-east-1 for tag value
    instances_stop = ec2.instances.filter(
        Filters = [{
            'Name' : 'tag:Action', 'Values': ['Auto-Stop']}
            ]
    )

    # Iterate through all instances in us-east-1 for tag value
    instances_start = ec2.instances.filter(
        Filters = [{
            'Name' : 'tag:Action', 'Values': ['Auto-Start']}
            ]
    )

    for inst in instances_start.all():
        inst.start()
        print('Started instances: ', inst.id)

    for instd in instances_stop.all():
        instd.stop()
        print('Stopped instances: ', instd.id)
