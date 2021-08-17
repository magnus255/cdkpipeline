import awsgi
from flask import (
    Flask,
    jsonify,
)

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify(status=200, message='OK')


def handler(event, context):
    # c = awsgi.response(app, event, context)
    # print(c)
    # return c

    return {
        'statusCode': "200",
        'body': {
            'x': event.__dict__,
            'y': context.__dict__
        },
    }