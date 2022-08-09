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
    $ pip install jupyter notebook
    ```
3. 在 CMD 輸入指令，啟動 jupyter notebook
    ```
    $ jupyter notebook
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
    $ pip install selenium
    ```
    ```
    $ pip install pandas
    ```
    ```
    $ pip install beautifulsoup4
    ```
    ```
    $ pip install lxml
    ```
    ```
    $ pip install requests
    ```

2. 一起安裝：
    1. 打開 CMD，進到專案資料夾 (操作方法見最下方)
    2. 在 CMD 執行下面指令
        ```
        $ pip install -r requirements.txt
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