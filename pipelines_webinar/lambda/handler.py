import awsgi
from w.w.wsgi import application


def handler(event, context):
    return awsgi.response(application, event, context)
