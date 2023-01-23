from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains
import time
# import re
from bs4 import BeautifulSoup
import pandas as pd
import requests
import os


def set_options():
    # 關閉通知
    options = webdriver.ChromeOptions()
    prefs = {
        'profile.default_content_setting_values':
            {
                'notifications': 2
            }
    }
    options.add_experimental_option('prefs', prefs) # 禁用瀏覽器彈窗
    options.add_argument("disable-infobars")    #瀏覽器上面跑的"Chrome正受到軟件控制"的字眼不顯示，但實際上跑起來還是有ㄟ
    options.add_argument("--headless")   # 最大化視窗

    return options

def crawl_shopee(kw_list,thr_list):
    options = set_options()
    driver = webdriver.Chrome(options=options)

    for keyword,thr in zip(kw_list,thr_list):
        driver.get(f"https://shopee.tw/search?keyword={keyword}&order=asc&page=0&sortBy=price")
        time.sleep(4)

        for i in range(7):
            # driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            # 隨便找個標籤對它按 page down 10次
            html = driver.find_element(By.TAG_NAME, 'html')
            html.send_keys(Keys.PAGE_DOWN)
            html.send_keys(Keys.RIGHT)
            html.send_keys(Keys.RIGHT)
            time.sleep(2)
        for i in range(8):
            html = driver.find_element(By.TAG_NAME, 'html')
            html.send_keys(Keys.LEFT)
            html.send_keys(Keys.LEFT)
            time.sleep(2)
        print("滑好了")
        
        #把HTML的資料全抓下來
        soup = BeautifulSoup(driver.page_source, "html.parser")
        analyze(soup, keyword,thr)

def analyze(soup, name,thr):
    all_ = soup.find_all("div", class_="shopee-search-item-result")
    all_result = all_[0].find_all("div", class_="col-xs-2-4 shopee-search-item-result__item")
    print(len(all_result))
    
    df = get_df(all_result,thr)
    
    df.to_excel(f"result/{name}.xlsx")
    df.to_html(f"result/{name}.html", escape=False, formatters=dict(Country=path_to_image_html))

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


def get_df(all_result,thr) -> pd.DataFrame:
    name_list = []
    img_list = []
    price_list = []
    sold_list = []
    href_list = []
    shopid_list = []
    user_list = []
    label_list = []


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
            sold = sold[4:]   # 移除字「已售出」
        if '-' in price:   # 將蝦皮的 price 用下面公式作區別
            if float(price.split('$')[1].split(' ')[0].replace(',','')) < int(thr): 
                label_list.append("●")
            else:
                label_list.append(" ")
        else:
            if float(price.split('$')[1].replace(',','')) < int(thr):
                label_list.append("●")
            else:
                label_list.append(" ")
        
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
        "username": user_list,
        "label" : label_list
    }

    df = pd.DataFrame(data)
    
    return df



def main():    
    kw_list = ["三多偉力健綜合優蛋白", "三多偉力健鉻營養素", "三多偉力健女性營養素", "三多偉力健LPN營養素",
                "三多偉力健關鍵營養素", "三多偉力健順暢營養素", "三多偉力健均衡營養素"]
    thr_list = [500]*7

    try:
        os.mkdir("result")
    except FileExistsError:
        pass

    start_time = time.time()
    crawl_shopee(kw_list,thr_list)
    end_time = time.time()
    print("total time =", end_time - start_time)


if __name__ == '__main__':
    main()