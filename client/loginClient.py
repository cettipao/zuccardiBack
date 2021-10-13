import requests


def get_auth_token(username: str, password: str):
    response = requests.post(
        "https://staging.omixom.com/api/get_auth_token/",
        data={"username": username, "password": password},
    )
    return response
