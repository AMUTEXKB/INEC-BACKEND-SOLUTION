from constructs import Construct
from aws_cdk import (
    aws_apigateway as apigw,
    aws_lambda as lambda_,
    aws_s3 as s3,
    aws_dynamodb as dynamodb,
    Stack
)


class InecStack(Stack):
    def __init__(self, scope:Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create an S3 bucket to store the uploaded images.
        bucket = s3.Bucket(self, "MyBucket",bucket_name="inec")

        # Create a DynamoDB table to store the uploaded data values.
        table = dynamodb.Table(
            self, "MyTable",
            table_name="inec",
            partition_key=dynamodb.Attribute(
                name="id",
                type=dynamodb.AttributeType.STRING
            )
        )

        # Create an API Gateway endpoint to receive the image and data values.
        api = apigw.RestApi(self, "InecApi",)

        # Create a Lambda function to handle the API Gateway request.
        handler = lambda_.Function(
            self, "MyFunction",
            runtime=lambda_.Runtime.PYTHON_3_8,
            function_name="inec_put_data",
            handler="lambda_function.lambda_handler",
            code=lambda_.Code.from_asset("inec/lambda/put_s3_dynamodb"),
            environment={
                "BUCKET_NAME": bucket.bucket_name,
                "TABLE_NAME": table.table_name
            }
        )
        # Create a Lambda function to handle the API Gateway request.
        get_s3= lambda_.Function(
            self, "MyFunction2",
            runtime=lambda_.Runtime.PYTHON_3_8,
            function_name="inec_get_s3",
            handler="lambda_function.lambda_handler",
            code=lambda_.Code.from_asset("inec/lambda/get_s3"),
            environment={
                "BUCKET_NAME": bucket.bucket_name,
                "TABLE_NAME": table.table_name
            }
        )
        # Create a Lambda function to handle the API Gateway request.
        get_dynamodb= lambda_.Function(
            self, "MyFunction3",
            runtime=lambda_.Runtime.PYTHON_3_8,
            function_name="inec_get_dynamodb",
            handler="lambda_function.lambda_handler",
            code=lambda_.Code.from_asset("inec/lambda/get_dynamodb"),
            environment={
                "BUCKET_NAME": bucket.bucket_name,
                "TABLE_NAME": table.table_name
            }
        )        

        # Grant the Lambda function permissions to access the S3 bucket and DynamoDB table.
        bucket.grant_read_write(handler)
        table.grant_read_write_data(handler)

        # Configure the API Gateway endpoint to integrate with the Lambda function.
        integration = apigw.LambdaIntegration(handler)
        api.root.add_method("PUT", integration)

        get_integration = apigw.LambdaIntegration(get_dynamodb)
        api.root.add_method("GET", get_integration)

        get_s3_integration = apigw.LambdaIntegration(get_s3)
        api.root.add_method("POST", get_s3_integration)        