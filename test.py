import os
import time
import requests
import pandas as pd

def get_items(kw, limit=60):
    url = f"https://shopee.tw/api/v4/search/search_items?by=price&keyword={kw}&limit={limit}&newest=0&order=asc&page_type=search&scenario=PAGE_GLOBAL_SEARCH&version=2"
    response = requests.request("GET", url)
    return response.json()["items"]

def main():
    response = get_items("三多葉黃素")
    print(len(response))

if __name__ == '__main__':
    print(123)
    main()
    print(456)