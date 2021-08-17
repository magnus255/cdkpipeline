import os
from os import path

from aws_cdk import (
    core as cdk,
    aws_lambda as lmb,
    aws_apigateway as apigw,
    aws_apigatewayv2 as apigw,
    aws_apigatewayv2_integrations as apigw_integration,
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
        #
        # lambda_role = iam.Role(self, 'LambdaRole',
        #                        assumed_by=iam.ServicePrincipal(
        #                            "lambda.amazonaws.com"))
        #
        # lambda_role.add_to_policy(
        #     iam.PolicyStatement(
        #         effect=iam.Effect.ALLOW,
        #         resources=['*'],
        #         actions=[
        #             "lambda:InvokeFunction"
        #         ]
        #     )
        # )

        handler = lmb.DockerImageFunction(
            self,
            "FastAPIImageLambda",
            code=lmb.DockerImageCode.from_image_asset(os.path.join(this_dir, 'lambda')),
        )

        # handler = lambda_python.PythonFunction(
        #     self, "Handler",
        #     entry=path.join(this_dir, 'lambda'),
        #     handler="handler",
        #     # optional, defaults to 'handler'
        #     runtime=lmb.Runtime.PYTHON_3_8,
        #     role=lambda_role,
        # )

        alias = lmb.Alias(self, 'Alias',
                          alias_name='Current',
                          version=handler.current_version,
                          )

        base_api = apigw.HttpApi(
            self,
            "FastAPIProxyGateway",
            api_name="FastAPIProxyGateway",
            default_integration=apigw_integration.LambdaProxyIntegration(
                handler=alias
            ),
        )
        #
        # gw = apigw.LambdaRestApi(
        #     self,
        #     'Gateway',
        #     description='Simple web',
        #     handler=alias
        # )

        # failure_alarm = cloudwatch.Alarm(
        #     self, 'Failure Alarm',
        #     metric=cloudwatch.Metric(
        #         metric_name='5XXError',
        #         namespace='AWS/ApiGateway',
        #         dimensions=dict(
        #             ApiName='Gateway'
        #         ),
        #         statistic='Sum',
        #         period=core.Duration.minutes(1),
        #     ),
        #     threshold=1,
        #     evaluation_periods=1
        # )

        # codedeploy.LambdaDeploymentGroup(self, 'DeploymentGroup',
        #                                  alias=alias,
        #                                  deployment_config=codedeploy.LambdaDeploymentConfig.ALL_AT_ONCE,
        #                                  alarms=[failure_alarm])

        core.CfnOutput(
            self, "EndpointUrl", value=base_api.api_endpoint,
            export_name="webinarApiUrl"
        )
