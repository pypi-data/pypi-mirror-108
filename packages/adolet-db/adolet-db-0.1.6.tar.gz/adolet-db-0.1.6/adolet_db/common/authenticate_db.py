import requests
from typing import Any, Dict


def authenticate_db(email: str, api_key: str) -> Dict[str, Any]:
    params = {'email': email, 'api_key': api_key}
    res = requests.get(
        'http://api.auth.adolet.com/authenticate',
        params=params,
    )
    res = res.json()

    database_url = {
        'dbname': res['dbname'],
        'user': res['user'],
        'password': res['password'],
        'host': res['host'],
        'port': res['port'],
    }
    return database_url
