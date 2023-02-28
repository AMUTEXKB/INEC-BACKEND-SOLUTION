import boto3
import json
import uuid

s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("MyTable")


def lambda_handler(event, context):
    # Extract data values from the API Gateway request.
    data = json.loads(event["body"])

    # Upload the image to the S3 bucket.
    key = str(uuid.uuid4())
    s3.put_object(Bucket="MyBucket", Key=key, Body=event["body"])

    # Insert the data values into the DynamoDB table.
    item = {
        "id": str(uuid.uuid4()),
        "name": data["name"],
        "description": data["description"],
        "image_url": f"https://s3.amazonaws.com/MyBucket/{key}"
    }
    table.put_item(Item=item)

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Data uploaded successfully."}) }