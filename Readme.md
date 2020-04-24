# The mini cloud

The idea:
I want a server where i can easily deploy hobby projects. 
* It needs to run at least ~10 webapplications
* Most need a databases
* some will have runners
* some need a messagebus

To do this, each app is a docker container. It can expose a http service. I will install a single nginx to act as a https proxy to the different applications using named virtualhosts

Since it is only a single server, i want to limit the amount of resources needed by "supporting services" such as databases and messagebusses. To do this, i will deploy a single mariadb instance, and a single rabbitmq instance. Each application can get separate credentials for these services.

Follow conventions of setting the environment DATABASE_URL to configure database connections.

Storage is done in volumes, preferably in /data

App code is in github
Github actions is used to 
* build a docker container
* upload it to docker hub

Then, i will build a custom management app where you can
* add applications based on a docker hub url
* add databases, storage and messagebusses to them
* update applications
* connect custom domains to applications
* backup databases and storage


cloud_manifest.json describes the application and what it needs. This file should be in the root of the image/container

Example cloud_manifest.json

```
name: myapp
expose:
- proto: http
  port: 80
needs:
- database
- messagebus
- storage
```

To extract it we can:
```
docker create <img>
docker cp <container>:/cloud_manifest.json .
```

The whole setup would include:
* an nginx instance
* an 'admin' instance with the admin gui (admin.[domain])
* a mariadb instance
* a rabbitmq instance

The install script can be as follows:

checksudo()
apt install -y docker.io
mkdir /cloud
cd /cloud
wget https://path.to/docker-compose.yml
docker-compose up -d


# Usefull things

python docker api:
https://docker-py.readthedocs.io/en/stable/

Github action to publish to docker hub:
https://github.com/marketplace/actions/publish-docker

