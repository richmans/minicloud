from flask import Flask, request, abort
from flask_restful import Resource, Api
import docker

client = docker.from_env()

app = Flask(__name__)
api = Api(app)

class ContainerList(Resource):
    def get(self):
        return [{"name": c.name, "status": c.status} for c in client.containers.list(True) if 'minicloud' in c.name]

class StopResource(Resource):
    def get(self, container_name):
        if not container_name.startswith("minicloud"):
            abort("Invalid container name")
        conts = [c for c in client.containers.list(True) if c.name == container_name]
        if len(conts):
            conts[0].stop()
        else:
            abort("Container not found")

class StartResource(Resource):
    def get(self, container_name):
        if not container_name.startswith("minicloud"):
            abort("Invalid container name")
        conts = [c for c in client.containers.list(True) if c.name == container_name]
        if len(conts):
            conts[0].start()
        else:
            abort("Container not found")

api.add_resource(ContainerList, '/')
api.add_resource(StopResource, '/stop/<string:container_name>')
api.add_resource(StartResource, '/start/<string:container_name>')

if __name__ == '__main__':
    app.run(host="0.0.0.0")