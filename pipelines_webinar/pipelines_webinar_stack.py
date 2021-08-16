from os import path

from aws_cdk import (
    core as cdk,
    aws_lambda as lmb,
    aws_ec2 as ec2,
    aws_apigateway as apigw,
    aws_cloudwatch as cloudwatch,
    aws_codedeploy as codedeploy,
)

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core


class PipelinesWebinarStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        this_dir = path.dirname(__file__)

        vpc = ec2.Vpc.from_lookup(
            self, "default_vpc", is_default=True
        )

        # lambda_security_group = ec2.SecurityGroup(
        #     self, "LambdaSecurityGroup", vpc=vpc
        # )

        handler = lmb.Function(
            self,
            'Handler',
            code=lmb.Code.from_asset(path.join(this_dir, 'lambda')),
            runtime=lmb.Runtime.PYTHON_3_8,
            handler='handler.handler',
        )
        lmb.CfnPermission(
            scope,
            "CrossAccountInvocationPermission",
            action="lambda:InvokeFunction",
            function_name=handler.function_name,
            principal="arn:aws:iam::333581294367:policy/InvokeLambdaPolicy",
        )

        alias = lmb.Alias(self, 'HandlerAlias', alias_name='LambdaAlias', version=handler.current_version)

        gw = apigw.LambdaRestApi(
            self,
            'Gateway',
            description='Simple web',
            handler=alias,
        )

        failure_alarm = cloudwatch.Alarm(
            self, 'FailureAlarm',
            metric=cloudwatch.Metric(
                metric_name='5XXError',
                namespace='AWS/ApiGateway',
                dimensions=dict(
                    ApiName='Gateway'
                ),
                statistic='Sum',
                period=core.Duration.minutes(1),
            ),
            threshold=1,
            evaluation_periods=1
        )

        codedeploy.LambdaDeploymentGroup(
            self, 'DeploymentGroup',
            alias=alias,
            deployment_config=codedeploy.LambdaDeploymentConfig.ALL_AT_ONCE,
            alarms=[failure_alarm],
        )

        self.url_output = core.CfnOutput(
            self,
            'Url',
            value=gw.url
        )
