import requests


def lzt_api_get_market_list(access_token, url):
    session = requests.session()
    session.headers = {
        'Authorization': f'Bearer {access_token}'
    }
    try:
        response = session.get(str(url).replace('lzt.market', 'api.lzt.market'))
    except requests.exceptions.RequestException:
        return None
    try:
        res = response.json().get("totalItems")
    except requests.exceptions.JSONDecodeError:
        return None
    if res is None:
        return None
    else:
        return response.json()
