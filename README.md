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
