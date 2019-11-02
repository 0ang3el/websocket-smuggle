#!/usr/bin/python

from flask import Flask, render_template, request, Response
from flask_socketio import SocketIO
from flask_restful import Resource, Api
from urlparse import urlparse
import requests

requests.packages.urllib3.disable_warnings()


app = Flask(__name__)
api = Api(app)
socketio = SocketIO(app, cors_allowed_origins='*', path='/api/public/socket.io')


class PublicProxyAPI(Resource):
    def get(self):
        return Response(status=405)

    def post(self):
        def check(_url):
            parsed = urlparse(_url)

            if parsed.port == 5000:
                return False

            if 'flag' in parsed.path.lower():
                return False

            bad = ('localhost', '127.', 'xip.io') # shitty check
            if any(w for w in bad if w in parsed.netloc.lower()):
                return False

            return True

        url = request.form.get('url')

        if not url:
            return {'message': 'Mandatory URL not specified'}, 400

        if not check(url):
            return {'message': 'Access to URL is denied'}, 403

        try:
            response = requests.get(url, allow_redirects=False, verify=False, timeout=40)
        except:
            return Response(status=500)

        return Response(status=response.status_code)


class Flag(Resource):
    def get(self):
        return {'flag': 'WHAt A WoNdeRFUL dAY for a cry OF De5p4iR ANd h3Ar7acH3'}


api.add_resource(Flag, '/flag')
api.add_resource(PublicProxyAPI, '/api/public/healthcheck')


@socketio.on('my event')
def handle_my_custom_event(json):
    #print('received json: ' + str(json))
    pass


if __name__ == '__main__':
    socketio.run(app, port=5000, host='127.0.0.1')

