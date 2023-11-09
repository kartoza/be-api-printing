# Create virtual enviroment 
- `python3 -m venv venv`

# Run virtual enviroment
- `source venv/bin/activate`

# Install packages
- `pip install -r requirements.txt`

# Run Flask App (Development)
- `cd api`
- `flask run`

# Sending request

- Url: `/print`
- Method: `POST`
- Body : ```
{
    "url": [],
    "download_path": ""
}
```

