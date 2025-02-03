from aws_cdk import (
    App, Stack,
    aws_lambda as lambda_,
    aws_apigateway as apigw,
    aws_dynamodb as dynamodb,
    aws_iam as iam,
    RemovalPolicy,
    aws_ecr as ecr
)

class AssignmentStack(Stack):
    def __init__(self, scope: App, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        table = dynamodb.Table(
            self, "MessagesTable",
            partition_key=dynamodb.Attribute(name="messageUUID", type=dynamodb.AttributeType.STRING),
            table_name="Messages",
            removal_policy=RemovalPolicy.DESTROY
        )

        lambda_role = iam.Role(
            self, "LambdaExecutionRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess")
            ]
        )

        lambda_function = lambda_.DockerImageFunction(
            self, "MessageProcessorLambda",
            code=lambda_.DockerImageCode.from_ecr(
                repository=ecr.Repository.from_repository_attributes(
                    self, "MyLambdaRepository",
                    repository_name="my-lambda-repository",
                    repository_arn="arn:aws:ecr:us-east-1:094895333954:repository/my-lambda-repository"
                ),
                tag="latest"
            ),
            role=lambda_role,
            environment={"TABLE_NAME": table.table_name}
        )

        api = apigw.LambdaRestApi(
            self, "MessagesApi",
            handler=lambda_function,
            proxy=False
        )

        messages_resource = api.root.add_resource("messages")
        messages_resource.add_method("POST")
