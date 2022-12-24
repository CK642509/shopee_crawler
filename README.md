![example workflow](https://github.com/CK642509/shopee_crawler/actions/workflows/main.yml/badge.svg)

# Startup

## Install
### 1. 安裝 Python
- 建議 3.9 以上
- [官網連結](https://www.python.org/)
- 不建議用最新的版本，怕還不穩定，目前推薦用[3.9.12](https://www.python.org/downloads/release/python-3912/)
- 上面點進去選擇「Windows installer (64-bit)」下載安裝，步驟原則上用預設，詳細步驟可以上網隨便找教學
- **Add Python 3.9 to PATH 要記得勾選!!!**



### 2. 安裝 jupyter notebook
1. 開啟命令提示字元 (搜尋「CMD」)
2. 輸入以下指令 (忽略$)
    ```
    pip install jupyter notebook
    ```
3. 在 CMD 輸入指令，啟動 jupyter notebook
    ```
    jupyter notebook
    ```
    > 使用 jupyter notebook 期間，CMD不能關閉

### 3. 下載這個專案
- 一般都是用 git 來 clone 專案下來，但你沒有要做版本控制的話就不需要這樣搞，直接下載壓縮檔下來解壓縮就好
- 下載方法：
    - 右上點選 code
    - 選擇 Download ZIP

### 4. 安裝 Python 套件
有5個套件需要安裝，可以一次安裝一個或是一起安裝
1. 一次安裝一個：

    在 CMD 依序執行下面四個指令
    ```
    pip install selenium
    ```
    ```
    pip install pandas
    ```
    ```
    pip install beautifulsoup4
    ```
    ```
    pip install lxml
    ```
    ```
    pip install requests
    ```

2. 一起安裝：
    1. 打開 CMD，進到專案資料夾 (操作方法見最下方)
    2. 在 CMD 執行下面指令
        ```
        pip install -r requirements.txt
        ```

### 5. 安裝 ChromeDriver
1. 在[這裡](https://chromedriver.chromium.org/downloads)下載 
2. 依據你的 chrome 版本選擇適當的 ChromeDriver
3. 下載後解壓縮，把檔案(`chromedriver.exe`)放進專案資料夾 (跟 `sentosa.ipynb`同個資料夾)

> ### **在哪裡查看 Chrome 版本？**
> 
> 打開 Chrome -> 設定 -> 關於 Chrome


### 6. 回到 Jupyter notebook，開始執行
1. 先前啟動 jupyter notebook 會在瀏覽器開啟資料夾目錄，進到 desktop後，選擇專案資料夾內的 `sentosa.ipynb` 執行


> ### **CMD 基本操作**
> 1. cd "資料夾名稱"
>    - 進入資料夾
>    - 註：打一個字母之後按tab可以自動補全，若有多個資料夾同樣開頭，則可以多按幾次tab
> 2. cd ..
>    - 回到上一層資料夾
> 3. 方向鍵「上」
>    - 顯示上次輸入的指令
>    - 註：再按會出現在前一次的指令

### 建立虛擬環境

```
pip install virtualenv
virtualenv .venv
```
## 讓 Github Actions 傳遞訊息(或檔案)
### Line Notify
#### 簡介
- `notify.py`是透過 [Line Notify](https://notify-bot.line.me/zh_TW/) 傳送 Line 訊息
- 只需要一個參數，即 Token 即可

#### 設定步驟
- 在 [Line Notify](https://notify-bot.line.me/zh_TW/) 登入後，從右上方進到個人頁面後，即可申請 Token
- 原則上訊息只能是下方這三種，不包含檔案(可參考[API文件](https://notify-bot.line.me/doc/en/))
    - 文字
    - 圖片 (url或檔案都可以)
    - 貼圖
- 由於需要讓程式碼取得 Token，因此透過 Github Actions 的 secret 來傳遞，設定方式如下
    - `notify.py` 內加入
        ```
        token = os.environ["LINE_NOTIFY_TOKEN"]
        ```
        其中 `INE_NOTIFY_TOKEN` 是自己定義的名稱
    
    - 在 .github/workflow 資料夾中的 `main.yml` 加入此步驟
        ```
        - name: test Line Notify
          env:
            LINE_NOTIFY_TOKEN: ${{ secrets.LINE_NOTIFY_TOKEN }}
          run: LINE_NOTIFY_TOKEN=$LINE_NOTIFY_TOKEN python notify.py
        ```
        透過此設定方式，才能將 Github Actions 中的 secret 以環境變數的方式送入 `notify.py`

- 若不想用 python 來幫助傳遞 Line Notify 訊息，也可以透過使用他人寫好的 actions 進行，例如[line-notify-actions](https://github.com/marketplace/actions/line-notify-actions)，設定方式如下
    - 在 .github/workflow 資料夾中的 `main.yml` 加入此步驟
        ```
        - name: send Line Notify message
        uses: louis70109/line-notify-action@master
        with:
            token: ${{ secrets.LINE_NOTIFY_TOKEN }}
            message: |
            From: ${{ github.event.sender.login }}
            image_file: 三多偉力健關鍵營養素.png
        ```

### Telegram
#### 簡介
- 相較於 Line Notify 無法傳遞檔案，Telegram 可以傳遞檔案，在使用上更加方便
- 需要機器人的 Token 和 聊天室 ID

#### 設定步驟
- 向 Telegram 的 [BotFather](https://t.me/BotFather) 進行對話 (指令為`/newbot`)，創立機器人，完成後即可取得機器人的 Token
- 接下來與機器人進行對話 (輸入任意訊息即可)，再進入這個網址
    ```
    https://api.telegram.org/botToken/getUpdates
    ```
    其中的網址中的`Token`請替換成上一步取得的機器人 Token
- 觀察回傳內容 (格式為`json`)，找出 `chat` 下的 `id` 的值，即為聊天室ID
- 最後只要在 Github Actions 中進行設定
    - 在 .github/workflow 資料夾中的 `main.yml` 加入此步驟
        ```
        - name: send Telegram message
        uses: appleboy/telegram-action@master
            with:
            to: ${{ secrets.TELEGRAM_CHAT_ID }}
            token: ${{ secrets.TELEGRAM_TOKEN }}
            message: |
                From: ${{ github.event.sender.login }}
            document: test.zip
            photo: 三多偉力健關鍵營養素.png
        ```
