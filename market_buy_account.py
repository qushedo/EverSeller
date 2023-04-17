import requests


def lzt_api_buy_account(access_token, item_id, price, fast_buy):
    session = requests.session()
    session.headers = {
        'Authorization': f'Bearer {access_token}'
    }
    val = 0
    if fast_buy:
        val = 1
    params = {'price': price, 'buy_without_validation': val}
    session.params = params
    try:
        response = session.post(f"https://api.lzt.market/{item_id}/fast-buy")
    except requests.exceptions.RequestException:
        return False
    try:
        print(response.json())
    except requests.exceptions.JSONDecodeError:
        return False
    if response.json().get("errors") is not None:
        return False
    return response.json()
