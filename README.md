docker build -t flask-tutorial:latest .

docker run -d -p 5000:5000 flask-tutorial

# iTask Restful API

## API Endpoints

* / [GET]
* /v1/auth/register      [POST]
* /v1/auth/login         [POST]
* /v1/projects           [GET, POST]
* /v1/projects/:id       [PATCH]
* /v1/projects/:id/tasks [GET, POST]
* /v1/projects/:id/users [GET]

## Databases

* users
* projects
* tasks
* roles
* user_roles
* assigned_tasks
* assigned_projects

## App Structure

.
├── Dockerfile
├── README.md
├── api
│   ├── __init__.py
│   ├── components
│   │   ├── base
│   │   │   ├── __init__.py
│   │   │   └── handler.py
│   │   ├── projects
│   │   │   ├── __init__.py
│   │   │   ├── handler.py
│   │   │   ├── model.py
│   │   │   └── schema.py
│   │   ├── tasks
│   │   │   ├── __init__.py
│   │   │   ├── handler.py
│   │   │   ├── model.py
│   │   │   └── schema.py
│   │   └── users
│   │       ├── __init__.py
│   │       ├── handler.py
│   │       ├── model.py
│   │       └── schema.py
│   ├── config
│   │   ├── auth.py
│   │   ├── config.py
│   │   ├── loader.py
│   │   ├── migrate.py
│   │   └── routes.py
│   ├── tests
│   └── utils
│       ├── __init__.py
│       ├── errors.py
│       └── logger.py
├── app.py
├── poetry.lock
└── pyproject.toml
