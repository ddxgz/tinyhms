Hospital Management System Server
================

## How to start the server
There are 2 ways to start up the server, the normal way and the docker way.

### Normal way
1. Install the requirements
```
pip3 install -r docker-compose/requirements.txt
```

2. Create the db file
```
python3 -m server.models
```

3. Start the server
```
python3 -m server.gateway
```

4. Start a redis server whether local or in a docker container

### Docker to setup server

The environment is organized as a docker container, locates in docker-compose/,
just docker-compose up. The port can be changed as you like in docker-compose.yml

To do this:
1. Install docker
```
$ wget -qO- https://get.docker.com/ | sh
```

2. Install docker-comopse
```
$ pip install docker-compose
```

Functions
---------------


Configuration
---------------


TODO
---------------
- Filter characters like space and other unwanted characters from requests data
- Expire time of token
- Encryption auth data
- Need a unique employee id to avoid duplicated registration.
- use a separated user auth module (may use the swift's tempauth like method, which uses memcache to store token, set a expire time on each token, or the auth middleware <https://github.com/talons/talons>)
- functest, probtest, unittest
- deal with the security of password storing and transferring


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
- Six >= 1.9
