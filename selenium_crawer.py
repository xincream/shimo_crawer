# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys


name_passwd = {
    'name': 'xuexin@guanghe.tv',
    'passwd': 'cyq940517'
}


def get_basic_info(driver, base_url, path):
    driver.get(base_url + path)
    print(driver.page_source)
    print(driver.current_url)
    email = driver.find_element_by_name('email')
    email.send_keys(name_passwd['name'])
    password = driver.find_element_by_name('password')
    password.send_keys(name_passwd['passwd'])
    driver.find_element_by_id('bd-login-submit').click()
    time.sleep(5)
    print(driver.current_url)


def get_desktop_info(driver, base_url, path):
    driver.get(base_url + path)
    print(driver.current_url)
    # print(driver.page_source)


def get_cookies(driver):
    cookie = [item["name"] + "=" + item["value"] for item in driver.get_cookies()]
    print(cookie)
    cookie_str = ';'.join(item for item in cookie)
    print(cookie_str)
    cookies = {}
    for line in cookie_str.split(';'):
        key, value = line.split('=', 1)  # 1代表只分一次，得到两个数据
        cookies[key] = value
    return cookies


def main():
    url = 'https://shimo.im'
    driver = webdriver.PhantomJS('/Users/one/Documents/phantomjs/bin/phantomjs')
    get_basic_info(driver, url, '/login')
    shimo_cookies = get_cookies(driver)
    driver.quit()
    print(shimo_cookies)
    return shimo_cookies


def test():
    url = 'https://shimo.im'
    # driver = webdriver.Chrome('/Users/one/Documents/chromedriver')
    driver = webdriver.PhantomJS('/Users/one/Documents/phantomjs/bin/phantomjs')
    driver.set_page_load_timeout(20)
    get_basic_info(driver, url, '/login')
    time.sleep(5)
    get_desktop_info(driver, url, '/desktop')
    shimo_cookies = get_cookies(driver)
    print(shimo_cookies)
    driver.quit()


if __name__ == '__main__':
    main()






