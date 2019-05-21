# Math Identifier Database  (MIB)

A standard django application that forms an information system
for Math Object Identifiers; see https://gitlab.com/IMKT/MOI for more information.

The system is deployed at http://moi.mathweb.org .

## Setup

**DO NOT DEPLOY ON PRODUCTION, USE PROPER WSGI FOR THAT**

1. Install python3, preferably create a virtualenv
2. ```python setup.py install -r requirements.txt```
3. ```python manage.py migrate```
4. ```python manage.py createsuperuser```


## Run
```python manage.py runserver```


## Docker

This repository contains a [Dockerfile](Dockerfile) which is designed to run the backend. 
By default, it listens on port 80 and uses an sqlite database stored in a volume mounted at `/data/`. 
An automated build is available under [kwarc/moi](https://hub.docker.com/r/kwarc/moi) and can be run with a command like the following:

```
   docker run -e DJANGO_SECRET_KEY=totally_secret_key_here -p 8000:80 -v data:/data/ kwarc/moi
```
