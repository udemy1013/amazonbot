from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading
import time

options = webdriver.ChromeOptions()
turnOnVNC = {"enableVNC": True}
options.set_capability("selenoid:options", turnOnVNC)

users = [["egi6ban@yahoo.co.jp", "kami5baaaan"], ["udemy1013@gmail.com", "tanoshiku1"], ["", ""]]

# Chromeをselenoidで立ち上げ
driver_twitter = webdriver.Remote(
    command_executor='http://localhost:4444/wd/hub',
    options=options
)

driver_amazon = webdriver.Remote(
    command_executor='http://localhost:4444/wd/hub',
    options=options
)

wait_twitter = WebDriverWait(driver_twitter, 10)
wait_amazon = WebDriverWait(driver_amazon, 10)


def amazon_login(email, password):
    # 指定のページに移動
    driver_amazon.get(
        "https://www.amazon.co.jp/dp/B08WB9FZ5D?_encoding=UTF8&m=AN1VRQENFRJN5&linkCode=sl1&tag=pokeyoyaku-22&linkId=b2879a95441ff1a013be62f774e62efa&language=ja_JP&ref_=as_li_ss_tl")

    # ログインボタンをクリック
    driver_amazon.find_element(By.XPATH, '//*[@id="nav-link-accountList"]').click()

    # メールアドレスをクリックして次へをクリック
    name_input = wait_amazon.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ap_email"]')))
    driver_amazon.find_element(By.XPATH, '//*[@id="ap_email"]').send_keys(email)
    driver_amazon.find_element(By.XPATH, '//*[@id="continue"]').click()

    name_input = wait_amazon.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ap_password"]')))
    driver_amazon.find_element(By.XPATH, '//*[@id="ap_password"]').send_keys(password)
    driver_amazon.find_element(By.XPATH, '//*[@id="signInSubmit"]').click()
    time.sleep(20)


def get_tweet():
    driver_twitter.get("https://twitter.com/pokecayoyaku")
    wait_twitter.until(EC.element_to_be_clickable((By.XPATH,
                                                   '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/section/div/div/div[2]/div/div/div/article/div/div/div/div[2]/div[2]/div[2]/div[1]/div/span[1]')))
    tweet_text = driver_twitter.find_element(By.XPATH,
                                             '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/section/div/div/div[2]/div/div/div/article/div/div/div/div[2]/div[2]/div[2]/div[1]/div/span[1]').text

    latest_time = return_seconds(driver_twitter.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/section/div/div/div[2]/div/div/div/article/div/div/div/div[2]/div[2]/div[1]/div/div/div[1]/div/div/div[2]/div/div[3]/a/time').text)

    print(latest_time)

    trying = True
    count = 0

    while trying:
        wait_twitter.until(EC.element_to_be_clickable((By.XPATH,
                                                       '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/section/div/div/div[2]/div/div/div/article/div/div/div/div[2]/div[2]/div[2]/div[1]/div/span[1]')))
        current_time = return_seconds(driver_twitter.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/section/div/div/div[2]/div/div/div/article/div/div/div/div[2]/div[2]/div[1]/div/div/div[1]/div/div/div[2]/div/div[3]/a/time').text)
        if count % 50 == 0:
            driver_amazon.refresh()
            print("amazon driverをリフレッシュ")

        # もし最新の投稿が最後の投稿より新しければ
        if current_time > latest_time:

            # フュージョンアーツかイーブイの投稿であればURLをクリックさせる
            if "フュージョン" in tweet_text or "イーブイ" in tweet_text:
                target_url = driver_twitter.find_element(By.XPATH,
                                                         '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/section/div/div/div[2]/div/div/div/article/div/div/div/div[2]/div[2]/div[2]/div[1]/div/a').text
                driver_amazon.get(target_url)
                print("HITTTTTTTTTTTT")
                wait_amazon.until(EC.element_to_be_clickable((By.XPATH,
                                                               '/html/body/div[2]/span/span/span/div/div/div[2]/div/div[1]/div/div[2]/div[3]/div/div[2]/span/span/span/span')))
                price = int("".join(filter(str.isdigit, driver_amazon.find_element(By.XPATH,  '/html/body/div[2]/span/span/span/div/div/div[2]/div/div[1]/div/div[2]/div[3]/div/div[2]/span/span/span/span').text)))
                print(price)
                if price < 5200:
                    trying = False
                    break
            # フュージョンアーツかイーブイの投稿でなければ最後の投稿時間を今の時間にする
            latest_time = current_time
            print("これは目的の投稿ではないよ")
        else:
            print("新しい投稿はまだだよ")
            driver_twitter.get("https://twitter.com/pokecayoyaku")
        count += 1


def buy_product():

    driver_amazon.find_element(By.XPATH, '/html/body/div[2]/span/span/span/div/div/div[2]/div/div[1]/div/div[2]/div[3]/div/div[2]/span/span/span/span').click()
    time.sleep(2)
    driver_amazon.find_element(By.XPATH, '//*[@id="aod-close"]/span/span').click()

    # 商品ページからカートページへ
    wait_amazon.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="nav-cart"]')))
    driver_amazon.find_element(By.XPATH, '//*[@id="nav-cart"]').click()

    # カートページ
    wait_amazon.until(
        EC.element_to_be_clickable((driver_amazon.find_element(By.XPATH, '//*[@id="sc-buy-box-ptc-button"]/span'))))
    driver_amazon.find_element(By.XPATH, '//*[@id="sc-buy-box-ptc-button"]/span').click()

    # 決済ページ
    wait_amazon.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="orderSummaryPrimaryActionBtn"]/span')))
    driver_amazon.find_element(By.XPATH, '//*[@id="orderSummaryPrimaryActionBtn"]/span').click()
    wait_amazon.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="submitOrderButtonId"]/span')))
    driver_amazon.find_element(By.XPATH, '//*[@id="submitOrderButtonId"]/span').click()


def return_seconds(text):

    result = 0
    text_letter = "".join(filter(str.isalpha, text))
    text_number = int("".join(filter(str.isdigit, text)))

    if text_letter == "h":
        return text_number * 60 * 60
    elif text_letter == "m":
        return text_number * 60
    elif text_letter == "s":
        return text_number


def scan(user_num):
    # target_price以下の値段であれば購入する
    target_price = 0
    target_button = ""

    # # 出品されている商品一覧をクリック
    # driver_amazon.find_element(By.XPATH, '//*[@id="olpLinkWidget_feature_div"]/div[2]/span/a').click()
    #
    # # 出品されている商品一覧を代入
    # wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="aod-offer-list"]')))
    #
    # driver_amazon.find_element(By.XPATH, '//*[@id="aod-filter-component"]').click()
    # wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="new"]/div/label/input')))
    # driver_amazon.find_element(By.XPATH, '//*[@id="new"]/div/label').click()
    # driver_amazon.find_element(By.XPATH, '//*[@id="aod-filter-component"]').click()
    #
    # time.sleep(5)
    #
    # product_list = driver_amazon.find_element(By.XPATH, '//*[@id="aod-offer-list"]')
    # product_lists = product_list.find_elements(By.XPATH, '//*[@id="aod-offer"]')
    #
    # num = 1
    #
    # for product in product_lists:
    #     current_price = int(product.find_element(By.XPATH, '//*[@id="aod-price-' + str(num) + '"]/span/span[2]/span[2]').text.replace(",", ""))
    #     if current_price < target_price:
    #         target_price = current_price
    #         target_button = product.find_element(By.XPATH, '//*[@id="aod-offer-price"]/div/div/div[2]/div/div/div[2]/span/span')
    #     num += 1
    #
    # target_button.click()
    # print(target_price)


# l1 = threading.Thread(target=main, args=(users[0][0], users[0][1]))
# l2 = threading.Thread(target=main, args=(users[1][0], users[1][1]))
# l1.start()
# l2.start()
amazon_login(users[1][0], users[1][1])
get_tweet()
buy_product()
time.sleep(60)
driver_amazon.quit()
driver_twitter.quit()
# time.sleep(15)
print("大成功")
