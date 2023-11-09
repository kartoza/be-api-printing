# Create virtual enviroment 
- `python3 -m venv venv`

# Run virtual enviroment
- `source venv/bin/activate`

# Install packages
- `pip install -r requirements.txt`

# Run Flask App
- `cd api`
- `python main.py`

# Sending request

- Url: `/print`
- Method: `POST`
- Body : ```
{
    "url": [],
    "download_path": ""
}
```

