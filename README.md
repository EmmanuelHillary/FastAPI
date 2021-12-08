# FastAPI
A small REST API blog app made with fastapi with CRUD functionalities and Authentication

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/EmmanuelHillary/FastAPI.git
$ cd FastAPI
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ py -3 -m venv env
$ env\Scripts\activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```
Note the `(env)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment 

Once `pip` has finished downloading the dependencies

create a database PostgreSQL/MySQL and a test database specifically called **test_db** to run test (`pytest -v`)

**Note** create a `.env` before running `pytest -v`

create a `.env` file and add the following below

```
DATABASE_USERNAME=(your database username)
DATABASE_PASSWORD=(your database password)
DATABASE_HOSTNAME=(your database Hostname)
DATABASE_PORT=(your database port)
DATABASE_NAME=(your database name)
SECRET_KEY=(create a secret key i.e(aghyg5dghjjgr56yghhyab5567b789nh789ngvf432xf3) )
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=(setup your token expiration time) 
```


make migrations and push the migrations

```sh
(env)$ alembic revision --autogenerate -m "made migrations"
(env)$ alembic upgrade head

``` 

then run the server

```sh
(env)$ uvicorn app.main:app
```
## Docs
And navigate to `http://127.0.0.1:8000/docs`

## Redoc
navigate to `http://127.0.0.1:8000/docs`


