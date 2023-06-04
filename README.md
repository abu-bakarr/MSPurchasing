# MSWebpurchasing

To get started with application, you must firs download [Python](https://www.python.org/)

## Project Start

create virtual environment

```sh
python -m venv env
```

### Active virtual environment

for windows

```sh
.\env\Scripts\activate
```

for Mac

```sh
source env/bin/activate
```

### Install all libraries

```sh
pip install -r requirements.txt
```

### Run the app

```sh
python manage.py runserver
```

### Access endpoint

```sh
BASE_URL =http://127.0.0.1:8000/api/

{
    "products": "http://127.0.0.1:8000/api/products/",
    "purchase-orders": "http://127.0.0.1:8000/api/purchase-orders/",
    "vendors": "http://127.0.0.1:8000/api/vendors/"
}
```
