import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('your_table_name')

response = table.get_item(
    Key={
        'id': 'your_item_id'
    }
)

item = response['Item']
