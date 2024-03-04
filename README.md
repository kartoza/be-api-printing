# Standalone install

## Create virtual enviroment 
- `python3 -m venv venv`

## Run virtual enviroment
- `source venv/bin/activate`

## Install packages
- `pip install -r requirements.txt`

## Run Flask App (Development)
- `cd api`
- `flask run`

# Docker install

1. `cd api`
2. `docker build -t api-app . `
3. `docker run -it -p 5000:5000 -d api-app`


# Sending request

- Url: `/print`
- Method: `POST`
- Body : ```
{
    "url": [],
    "download_path": ""
}
```

