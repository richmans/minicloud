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

# Admin app architecture
The admin app consists of 3 processes:
* An nginx process acting as the main http/https webserver
* A django app offering a GUI app to the admin. It stores info in the database and puts commands in the rabbitmq queue
* A python runner app that executes commands:
  * (re)deploy an app on docker with env vars from the db
  * provision credentials for rabbitmq or mariadb
  * render nginx configurationfiles based on the db and reload nginx

cloud_manifest.yml describes the application and what it needs. Docker seems to solve part of this problem, for it describes an EXPOSE command for defining open ports, but it doesn't seem to have a way of describing what services a container depends on. I also could not think of a way to mis-use standard docker features to this. So, i decided to define cloud_manifest.yml

Example cloud_manifest.yml

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
export CONTAINER=`docker create richmans/minidemo`
docker cp $CONTAINER:/cloud_manifest.yml .
docker rm $CONTAINER
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

# Useful things

python docker api:
https://docker-py.readthedocs.io/en/stable/

Github action to publish to docker hub:
https://github.com/marketplace/actions/publish-docker
-> Insight: this is not needed. Docker hub provides webhook integration with github. A push to github initiates a docker hub build and publish. Easy!

A small demo app to test deployments:
https://hub.docker.com/repository/docker/richmans/minidemo

Python lib to generate nginx config
https://github.com/peakwinter/python-nginx

Heroku app json
https://devcenter.heroku.com/articles/app-json-schema#addons

# Server setup
In digitalocean, choose the docker image from them marketplace. For size, i started with the smallest ($5) instance. Works great so far, haven't really tested the limits of how much this can host.

```
git clone https://github.com/richmans/minicloud
cd minicloud
./generate_env.sh
docker-compose up -d
```
