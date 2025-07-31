import boto3

def lambda_handler(event, context):
    s3 = boto3.client('s3')

    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

        print(f"Tagging object: {bucket}/{key}")

        s3.put_object_tagging(
            Bucket=bucket,
            Key=key,
            Tagging={
                'TagSet': [
                    {'Key': 'Project', 'Value': 'Auto-Tagged'},
                    {'Key': 'Environment', 'Value': 'Dev'}
                ]
            }
        )

    return {
        'statusCode': 200,
        'body': 'Tags applied successfully!'
    }
