from aws_cdk import (
    core,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as cpations,
    pipelines,
)


class PipelineStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        source_artifact = codepipeline.Artifact()
        cloud_assymble_artifact = codepipeline.Artifact()

        pipelines.CdkPipeline(
            self,
            'Pipeline',
            cloud_assembly_artifact=cloud_assymble_artifact,
            pipeline_name='WebinarPipeline',
            source_action=cpations.GitHubSourceAction(
                action_name='Github',
                output=source_artifact,
                oauth_token=core.SecretValue.secrets_manager('github-token'),
                owner='magnus255',
                repo='cdkpipeline',
                trigger=cpations.GitHubTrigger.POLL,
            ),
            synth_action=pipelines.SimpleSynthAction(
                source_artifact=source_artifact,
                cloud_assembly_artifact=cloud_assymble_artifact,
                install_command='npm install -g aws-cdk && pip install -r requirements.txt',
                synth_command='cdk synth',
            )
        )