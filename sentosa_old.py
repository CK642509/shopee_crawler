from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains
import time
# import re
from bs4 import BeautifulSoup
from lxml import etree
import pandas as pd
import requests

def set_options():
    # 關閉通知
    options = webdriver.ChromeOptions()
    prefs = {
        'profile.default_content_setting_values':
            {
                'notifications': 2
            }
    }
    options.add_experimental_option('prefs', prefs)
    options.add_argument("disable-infobars")
    options.add_argument("--start-maximized")   # 最大化視窗

    return options

def crawl_shopee(kw_list):
    options = set_options()
    driver = webdriver.Chrome(options=options)

    for keyword in kw_list:
        driver.get(f"https://shopee.tw/search?keyword={keyword}&order=asc&page=0&sortBy=price")
        time.sleep(4)

        for i in range(10):
            # driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            # 隨便找個標籤對它按 page down
            html = driver.find_element(By.TAG_NAME, 'html')
            html.send_keys(Keys.PAGE_DOWN)
            time.sleep(1)
        print("滑好了")
        
        html = etree.HTML(driver.page_source)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        analyze(soup, keyword)

def analyze(soup, name):
    all_ = soup.find_all("div", class_="shopee-search-item-result")
    all_result = all_[0].find_all("div", class_="col-xs-2-4 shopee-search-item-result__item")
    print(len(all_result))
    
    df = get_df(all_result)
    
    df.to_excel(f"{name}.xlsx")
    df.to_html(f"{name}.html", escape=False, formatters=dict(Country=path_to_image_html))

def path_to_image_html(path):
    return '<img src="'+ path + '" width="100" >'

def href_to_full_path(href):
    return f'<a href="https://shopee.tw{href}">link</a>'

def get_username_by_shopid(id):
    url = f"https://shopee.tw/api/v4/product/get_shop_info?shopid={id}"
    response = requests.request("GET", url)

    try:
        return response.json()["data"]["account"]["username"]
    except:
        return ""


def get_df(all_result) -> pd.DataFrame:
    name_list = []
    img_list = []
    price_list = []
    sold_list = []
    href_list = []
    shopid_list = []
    user_list = []


    for product in all_result:
        try:
            name = product.find_all("div", class_="ie3A+n bM+7UW Cve6sh")[0].text
        except:
            name = ""

        try:
            img = product.find_all("img", {"class": ["_7DTxhh", "vc8g9F"]})[0]["src"]
        except:
            img = ""

        try:
            price = product.find_all("div", {"class": ["vioxXd", "rVLWG6h"]})[0].text
        except:
            price = ""

        try:
            sold = product.find_all("div", {"class": ["r6HknA", "uEPGHT"]})[0].text
        except:
            sold = ""

        try:
            href = product.find_all("a", {"data-sqe": "link"})[0]["href"]
        except:
            href = ""

        if sold != "":
            sold = sold[4:]   # 移除「已售出」
        
        # 先用 ?sp_atk= 切，取第一段
        # 再用 . 切，取倒數第二段
        shopid = href.split("?sp_atk=")[0].split(".")[-2]

        username = get_username_by_shopid(shopid)

        name_list.append(name)
        img_list.append(path_to_image_html(img))
        price_list.append(price)
        sold_list.append(sold)
        href_list.append(href_to_full_path(href))
        shopid_list.append(shopid)
        user_list.append(username)

    data = {
        "name": name_list,
        "img": img_list,
        "price": price_list,
        "sold": sold_list,
        "href": href_list,
        "shopid": shopid_list,
        "username": user_list
    }

    df = pd.DataFrame(data)
    
    return df



def main():    
    kw_list = ["三多偉力健關鍵營養素", "三多偉力健鉻營養素"]
    # kw_list = ["三多偉力健關鍵營養素"]

    start_time = time.time()
    crawl_shopee(kw_list)
    end_time = time.time()
    print("total time =", end_time - start_time)


if __name__ == '__main__':
    main()
