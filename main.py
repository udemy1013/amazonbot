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

users = [["egi6ban@yahoo.co.jp", "kami5ban"], ["udemy1013@gmail.com", "tanoshiku1"], ["", ""]]

# Chromeをselenoidで立ち上げ


def main(email, password):

    driver = webdriver.Remote(
        command_executor='http://localhost:4444/wd/hub',
        options=options
    )

    wait = WebDriverWait(driver, 10)

    # 指定のページに移動
    driver.get("https://www.amazon.co.jp/dp/B08WB9FZ5D?_encoding=UTF8&m=AN1VRQENFRJN5&linkCode=sl1&tag=pokeyoyaku-22&linkId=b2879a95441ff1a013be62f774e62efa&language=ja_JP&ref_=as_li_ss_tl")

    # ログインボタンをクリック
    driver.find_element(By.XPATH, '//*[@id="nav-link-accountList"]').click()

    # メールアドレスをクリックして次へをクリック
    name_input = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ap_email"]')))
    driver.find_element(By.XPATH, '//*[@id="ap_email"]').send_keys(email)
    driver.find_element(By.XPATH, '//*[@id="continue"]').click()

    name_input = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ap_password"]')))
    driver.find_element(By.XPATH, '//*[@id="ap_password"]').send_keys(password)
    driver.find_element(By.XPATH, '//*[@id="signInSubmit"]').click()
    time.sleep(3)

    trying = True

    while trying:
        try:
            driver.find_element(By.XPATH,
                                '//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span/span[2]/span[2]').click()
        except:
            driver.get(
                "https://www.amazon.co.jp/dp/B08WB9FZ5D?_encoding=UTF8&m=AN1VRQENFRJN5&linkCode=sl1&tag=pokeyoyaku-22&linkId=b2879a95441ff1a013be62f774e62efa&language=ja_JP&ref_=as_li_ss_tl")
        else:
            driver.find_element(By.XPATH, '//*[@id="submit.buy-now"]').click()
            trying = False

    # # メイン商品の価格を抽出
    # core_price = int(
    #     driver.find_element(By.XPATH, '//*[@id="corePrice_feature_div"]/div/div/span/span[2]/span[2]').text.replace(",",
    #                                                                                                                 ""))
    # target_price = 5200
    # while core_price > target_price:
    #     if core_price < target_price:
    #         break
    #     else:
    #         driver.get("https://www.amazon.co.jp/dp/B08WB9FZ5D?_encoding=UTF8&m=AN1VRQENFRJN5&linkCode=sl1&tag=pokeyoyaku-22&linkId=b2879a95441ff1a013be62f774e62efa&language=ja_JP&ref_=as_li_ss_tl")
    #         wait.until(
    #             EC.element_to_be_clickable((By.XPATH, '//*[@id="corePrice_feature_div"]/div/div/span/span[2]/span[2]')))
    #         core_price = int(driver.find_element(By.XPATH,
    #                                              '//*[@id="corePrice_feature_div"]/div/div/span/span[2]/span[2]').text.replace(
    #             ",", ""))
    #         print("try again")

    # driver.find_element(By.XPATH, '//*[@id="submit.buy-now"]').click()
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="submitOrderButtonId"]/span')))
    driver.find_element(By.XPATH, '//*[@id="submitOrderButtonId"]/span').click()
    print("イーブイヒーローズが買えたよ")


def scan(user_num):
    # target_price以下の値段であれば購入する
    target_price = 0
    target_button = ""

    # # 出品されている商品一覧をクリック
    # driver.find_element(By.XPATH, '//*[@id="olpLinkWidget_feature_div"]/div[2]/span/a').click()
    #
    # # 出品されている商品一覧を代入
    # wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="aod-offer-list"]')))
    #
    # driver.find_element(By.XPATH, '//*[@id="aod-filter-component"]').click()
    # wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="new"]/div/label/input')))
    # driver.find_element(By.XPATH, '//*[@id="new"]/div/label').click()
    # driver.find_element(By.XPATH, '//*[@id="aod-filter-component"]').click()
    #
    # time.sleep(5)
    #
    # product_list = driver.find_element(By.XPATH, '//*[@id="aod-offer-list"]')
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


l1 = threading.Thread(target=main, args=(users[0][0], users[0][1]))
l2 = threading.Thread(target=main, args=(users[1][0], users[1][1]))
l1.start()
l2.start()
time.sleep(15)
print("大成功")
