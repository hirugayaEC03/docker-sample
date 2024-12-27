import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import streamlit as st
import requests

# Selenium用のChromeオプションを設定
def set_chrome_options():
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    return chrome_options

# Selenium Gridを利用して画像を取得
def download_images_from_url(url):
    selenium_hub_url = os.getenv("SELENIUM_GRID_URL")  # 環境変数から取得
    chrome_options = set_chrome_options()
    driver = webdriver.Remote(command_executor=selenium_hub_url, options=chrome_options)
    
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'o-productdetailvisual_thumb'))
        )
        elements = driver.find_elements(By.CLASS_NAME, 'o-productdetailvisual_thumb')
        image_urls = [el.get_attribute('data-mainsrc') for el in elements if el.get_attribute('data-mainsrc')]
    finally:
        driver.quit()
    
    return image_urls

# Streamlitアプリケーション
def main():
    st.title("画像ダウンロードアプリ")
    url = st.text_input("画像URLを入力してください")
    if st.button("ダウンロード"):
        if url:
            st.write("画像の取得を開始します...")
            try:
                image_urls = download_images_from_url(url)
                for image_url in image_urls:
                    st.write(f"取得した画像: {image_url}")
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
        else:
            st.warning("URLを入力してください")

if __name__ == "__main__":
    main()

