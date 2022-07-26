# Stock Market API

Example API to get market data related to stocks.

## How it works?

This service has two APIs:

- Signup: It allows to get an API key by sending user credentials (email, password, name, last name). If your email is already registered, you will need to send the password you set previously to get your API key again.

- Stocks: It allows to get information about certain stock, you will need to specify a stock symbol in the url. IMPORTANT: You need to add your API key in the authorization header to consume this, e.g 'Authorization Bearer YOUR_API_KEY'

## API Documentation

A basic API documentation can be found here https://matisotee-stocks-api.herokuapp.com

## Heroku deployed service

Everyone can consume the APIs hosted in Heroku:

- POST https://matisotee-stocks-api.herokuapp.com/sign_up/
- GET https://matisotee-stocks-api.herokuapp.com/stocks/<stock_symbol>


## Local Installation

There are two different ways to install the app locally:

- Docker
- Normal python installation

### Docker Installation

Prerequisites: Docker installed

1) Clone the repo

2) Build image

```bash
docker build -t stock_market:latest .
```

3) Run container

```bash
docker run --name stock_market -p 127.0.0.1:8000:8000/tcp stock_market:latest
```

### Python Installation

Prerequisites: Python 3.10 installed

1) Clone the repo

2) Create virtual env:

```bash
python3 -m venv env
```
3) Activate virtual env:

```bash
source env/bin/activate
```

4) Install dependencies

```bash
pip3 install -r requirements.txt
```

5) Run Django migrations

```bash
python3 manage.py migrate
```

6) Run server

```bash
python3 manage.py runserver
```

## Testing

Unit tests can be run locally. If you already cloned the repo and installed the project dependencies just execute the command:
```bash
pytest
```

## Feature summary

Some extra features implemented in this repo are:

- API Throttling: There is a limit of 4 requests per minute.
- Logging: All the requests are logged in the server.
