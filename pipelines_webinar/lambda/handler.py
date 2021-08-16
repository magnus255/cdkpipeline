import awsgi
from w.w.wsgi import application


def handler(event, context):
    x = awsgi.response(application, event, context)
    return {
        'body': x,
        'statusCode': '200',
    }
