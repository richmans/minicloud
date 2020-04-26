from flask import Flask, request
from flask_restful import Resource, Api
import docker

client = docker.from_env()

app = Flask(__name__)
api = Api(app)

greetings = {'world': 'hello world'}

class Greeting(Resource):
    def get(self, greeting_id):
        return greetings[greeting_id]

    def put(self, greeting_id):
        greetings[greeting_id] = request.form['greeting']
        return {greeting_id: greetings[greeting_id]}

class ContainerList(Resource):
    def get(self):
        return [c.name for c in client.containers.list()]

api.add_resource(ContainerList, '/containers')
api.add_resource(Greeting, '/<string:greeting_id>')

if __name__ == '__main__':
    app.run(host="0.0.0.0")