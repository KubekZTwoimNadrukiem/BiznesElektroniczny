import requests
import base64
from bs4 import BeautifulSoup


from endpoint import Endpoint


def encode_key(username = "", password = ""):
    return base64.b64encode(f"{username}:{password}".encode()).decode()


def get_endpoints(api_url, header):
    endpoints = {}
    response = requests.get(api_url, headers=header)
    if response.status_code != 200:
        print(f"Couldn't get endpoints ({response.status_code}).")
        return endpoints

    bs_data = BeautifulSoup(response.text, "xml")
    shop_name = "Yarnstreet"
    prestashop = bs_data.find("api", {"shopName": shop_name})
    for child in prestashop.children:
        if child is None or child.name is None:
            continue

        path = child.attrs['xlink:href']
        get = child.attrs['get'] == 'true'
        put = child.attrs['put'] == 'true'
        post = child.attrs['post'] == 'true'
        delete = child.attrs['delete'] == 'true'
        head = child.attrs['head'] == 'true'
        endpoint = Endpoint(path, child.name.strip(), get, put, post, delete, head)
        endpoints[child.name.strip()] = endpoint

    return endpoints

