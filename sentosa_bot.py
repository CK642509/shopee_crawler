import os
import time
import requests
import pandas as pd

def get_items(kw, limit=60):
    url = f"https://shopee.tw/api/v4/search/search_items?by=price&keyword={kw}&limit={limit}&newest=0&order=asc&page_type=search&scenario=PAGE_GLOBAL_SEARCH&version=2"
    response = requests.request("GET", url)
    return response.json()["items"]

def get_username_by_shopid(id):
    url = f"https://shopee.tw/api/v4/product/get_shop_info?shopid={id}"
    response = requests.request("GET", url)

    try:
        return response.json()["data"]["account"]["username"]
    except:
        return ""

def img_to_html(img):
    return f'<img src="https://cf.shopee.tw/file/{img}_tn" width="100">'

def href_to_html(href):
    return f'<a href="{href}">link</a>'

def analyze_items(items: list, thr: int) -> pd.DataFrame:
    img_list = []
    name_list = []
    price_list = []
    sold_list = []
    href_list = []
    shopid_list = []
    user_list = []
    label_list = []

    for item in items:
        img = item["item_basic"]["image"]
        name = item["item_basic"]["name"]
        
        sold = item["item_basic"]["historical_sold"]
        price = item["item_basic"]["price_min"] / 100000   # 原始數據後面有5個0
        # price_max = item["item_basic"]["price_max"]
        shopid = item["item_basic"]["shopid"]
        itemid = item["item_basic"]["itemid"]
        
        username = get_username_by_shopid(shopid)

        href = f"https://shopee.tw/{name.replace(' ', '-')}-i.{shopid}.{itemid}"

        name_list.append(name)
        shopid_list.append(shopid)
        sold_list.append(sold)
        price_list.append(price)
        img_list.append(img_to_html(img))
        user_list.append(username)
        href_list.append(href_to_html(href))

        if price <= thr:
            label_list.append("●")
        else:
            label_list.append(" ")

    _min = min(price_list)

    data = {
        "img": img_list,
        "name": name_list,
        "price": price_list,
        "min": _min,
        "sold": sold_list,
        "href": href_list,
        "shopid": shopid_list,
        "username": user_list,
        "label": label_list
    }

    df = pd.DataFrame(data)
    df2 = df.sort_values(by=["price"])
    
    return df2

def shopee_crawl(kw_list, thr_list):
    for keyword, thr in zip(kw_list, thr_list):
        items = get_items(keyword)
        print(keyword, len(items))

        df = analyze_items(items, thr)
        df_2 = df.drop(columns=['img', 'href'])
        df_3 = df_2.loc[df['label'] == "●"]
        df_4 = df_3.drop(columns=['label'])
        print(df_4)

        # df.to_excel(f"result/{keyword}.xlsx")
        # df.to_html(f"result/{keyword}.html", escape=False, formatters=dict(Country=img_to_html))


def main():   
    kw_list = ["三多偉力健綜合優蛋白", "三多偉力健鉻營養素", "三多偉力健女性營養素", "三多偉力健LPN營養素",
                "三多偉力健關鍵營養素", "三多偉力健順暢營養素", "三多偉力健均衡營養素"]
    # kw_list = ["三多偉力健關鍵營養素"]
    thr_list = [500]*7

    # create folder
    try:
        os.mkdir("result")
    except FileExistsError:
        pass

    start_time = time.time()
    shopee_crawl(kw_list, thr_list)
    end_time = time.time()
    print("total time =", end_time - start_time)


if __name__ == '__main__':
    main()
