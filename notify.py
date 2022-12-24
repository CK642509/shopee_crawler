import requests
import os

token = os.environ.LINE_NOTIFY_TOKEN

# 要發送的訊息
message = '這是用 Python 發送的訊息與圖片'

# HTTP 標頭參數與資料
headers = { "Authorization": "Bearer " + token }
data = { 'message': message }

# 要傳送的圖片檔案
image = open('Teemo.png', 'rb')
files = { 'imageFile': image }

# 以 requests 發送 POST 請求
requests.post("https://notify-api.line.me/api/notify",
    headers = headers, data = data, files = files)