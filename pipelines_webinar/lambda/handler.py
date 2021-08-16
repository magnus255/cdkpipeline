import awsgi
from w.w.wsgi import application


def handler(event, context):
    try:
        return awsgi.response(application, event, context)
    except Exception as exc:
        return {
            'body': str(exc),
            'statusCode': '200',
        }
