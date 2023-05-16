import time

import requests


def lzt_api_get_user_name(access_token):
    session = requests.session()
    session.headers = {
        'Authorization': f'Bearer {access_token}'
    }
    try:
        response = session.get(
            "https://api.lzt.market/me"
        )
    except requests.exceptions.RequestException:
        return ["WRONG TOKEN / ERROR", "WRONG TOKEN / ERROR", "WRONG TOKEN / ERROR", "ERROR"]
    try:
        res = response.json().get("user")
    except requests.exceptions.JSONDecodeError:
        return ["WRONG TOKEN / ERROR", "WRONG TOKEN / ERROR", "WRONG TOKEN / ERROR", response.text]
    if res is None or response.json().get("error") is not None:
        return ["WRONG TOKEN / ERROR", "WRONG TOKEN / ERROR", "WRONG TOKEN / ERROR", response.text]
    else:
        return [res.get("username"), res.get("short_link"), res.get("balance"), response.text]