Hospital Management System Server
================

Functions
---------------


Configuration
---------------


TODO
---------------
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
The environment is organized as a docker container, locates in docker-compose/,
just docker-compose up. The port can be changed as you like in docker-compose.yml

- Python >= 2.7 or 3.4
- Gunicorn
- Falcon >= 0.3.0
- peewee >= 2.6.1
- Six >= 1.9
