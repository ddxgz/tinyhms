Hospital Management System Server
================
Docs in docs folder or http://pa2515-hms-server.readthedocs.org/en/

## How to start the server
There are 2 ways to start up the server, the normal way and the docker way.


### Use Docker to setup server

The environment is organized as a docker container, locates in docker-compose/,
just docker-compose up. The port can be changed as you like in docker-compose.yml

To do this:

- Install docker (Or check on docker's official website to find how to install docker on your operating system)
```
$ wget -qO- https://get.docker.com/ | sh
```

- Install docker-comopse
```
$ pip install docker-compose
```

- Make the Swift docker to run

    - data container
    ```
    docker run -v /srv --name SWIFT_DATA busybox
    ```

    - Swift container
    ```
    ID=$(docker run -d -p 8081:8080 --volumes-from SWIFT_DATA -t morrisjobke/docker-swift-onlyone)
    ```

- Run the docker container of server with redis, go to the docker-compose/, run:
```
docker-compose up
```
or try if with sudo

It will take some time to download the images and install dependencies.


### The Normal way

- Install the requirements
```
pip3 install -r docker-compose/requirements.txt
```

- Create the db file
```
python3 -m server.models
```

- Start the server 
```
python3 -m server.gateway
```

- Start a redis server whether local or in a docker container


Functions
---------------


Configuration
---------------


TODO
---------------
- Filter characters like space and other unwanted characters from requests data
- Expire time of token
- Encryption auth data
- ~~Need a unique employee id to avoid duplicated registration.~~
- ~~use a separated user auth module (may use the swift's tempauth like method, which uses memcache to store token, set a expire time on each token, or the auth middleware <https://github.com/talons/talons>)~~
- ~~functest, probtest, unittest~~
- ~~deal with the security of password storing and transferring~~


BUG
---------------



Notice
---------------


Requirements
---------------
- Python >= 2.7 or 3.4
- Gunicorn
- Falcon >= 0.3.0
- peewee >= 2.6.1
- swiftclient >= 2.7.0
- redis
- Six >= 1.9

Test Requirements
---------------
- Python >= 2.7 or 3.4
- Falcon >= 0.3.0
- peewee >= 2.6.1
- swiftclient >= 2.7.0
- requests >= 2.8.1
- redis
- Six >= 1.9
