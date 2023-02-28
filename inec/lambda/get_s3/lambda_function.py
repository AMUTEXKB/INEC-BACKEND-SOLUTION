import boto3

s3 = boto3.client('s3')

bucket_name = 'your_bucket_name'
key = 'your_key'

response = s3.get_object(Bucket=bucket_name, Key=key)

data = response['Body'].read()
