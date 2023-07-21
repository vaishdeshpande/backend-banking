# Backend bank transactions by using FastAPI

The application is developed using FastAPI and PostgreSQL. It allows users to perform various banking operations, such as creating accounts, making deposits, and performing withdrawals. The system is organized into several files, each serving a specific purpose which is mentioned as comments at the top.

##### This API has 5 routes

#### 1) Create Account (Post route)

##### This route is reponsible for creating post, deleting post, updating post and Checkinh post

#### 2) Add Account Type (Post route)

##### This route is about creating users and searching user by id

#### 3) Deposit (PUT route)

##### This route is about login system

#### 4) Withdraw (PUT route)

##### This route is about likes or vote system and this route contain code for upvote or back vote there is not logic about down vote

#### how to run locally

First clone this repo by using following command

```

git clone https://github.com/vaishdeshpande/backend-banking.git

```

then

```

cd backend-banking

```

then

```
docker-compose build

docker-compose up -d
```

Then you can use following link to use the API

```
http://127.0.0.1:8000/docs

```

Entrypoint Of the Application:

```
main.py
```
