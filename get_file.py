# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import shimo_crawer.selenium_crawer as sc
import shimo_crawer.txt_html as th
import shimo_crawer.save_db as sb
from bs4 import BeautifulSoup
import requests
import re
import os
import codecs


def test_cookies(shimo_cookies):
    test_url = 'https://shimo.im/doc/yK1973TsCOEbR4Cv'  # 'https://shimo.im/doc/r19moXP5jucnSdu1'
    r = requests.get(test_url, cookies=shimo_cookies)
    print(r.url)
    soup = BeautifulSoup(r.text, 'lxml')
    print(soup.prettify())
    print(soup.find('title').text)
    s_dict = resolve_html(r.text)
    print(s_dict['name'])
    print(s_dict['content'])
    content = eval(s_dict['content'])['text']
    print(content)
    to_txt(s_dict['name'], r.url, content)


def get_all_file_path(url, shimo_cookies, names):
    temp_url = url + '/' + names[0]
    folders1 = get_all_folder(temp_url, shimo_cookies)
    print(folders1)
    folder_url1 = url + '/folder/' + folders1[names[1]]
    folders2 = get_all_folder(folder_url1, shimo_cookies)
    print(folders2)
    folder_url2 = url + '/folder/' + folders2[names[2]]
    files = get_all_file(folder_url2, shimo_cookies)
    print(files)
    return [url + '/doc/' + item for item in files]


def get_all_folder(url, shimo_cookies):
    r = requests.get(url, cookies=shimo_cookies)
    s_dict = resolve_html(r.text)
    folders = {item['name']: item['guid'] for item in s_dict['children'] if item['is_folder'] == 1}
    return folders


def get_all_file(url, shimo_cookies):
    r = requests.get(url, cookies=shimo_cookies)
    s_dict = resolve_html(r.text)
    files = [item['guid'] for item in s_dict['children'] if item['is_folder'] == 0]
    return files


def get_file_info(url, shimo_cookies, to_html):
    r = requests.get(url, cookies=shimo_cookies)
    s_dict = resolve_html(r.text)
    name = s_dict['name']
    content = eval(s_dict['content'])['text']
    if to_html:
        content = th.shimo_format(content)
    return name, url, content


def resolve_html(text):
    elem = re.findall(r'tempCurrentFile: {.+?originalUrl', text, re.S)[0]
    elem = re.sub(r',\n.+?originalUrl', '', elem, re.S)
    s_dict = eval(elem.replace(r'tempCurrentFile: ', '')
                  .replace('true', 'True').replace('false', 'False').replace('null', 'None'))
    return s_dict


def to_txt(name, url, content):
    file_name = 'data/' + name + '.txt'
    if not os.path.exists('data/'):
        os.mkdir('data/')
    with codecs.open(file_name, 'w', 'utf-8') as f:
        f.write(name + '\n')
        f.write(url + '\n')
        f.write(content + '\n')


def save_all(to_html, to_db):
    cookies = sc.main()
    base_url = 'https://shimo.im'
    folder_name = ['desktop', '数据组', '散需求']
    file_paths = get_all_file_path(base_url, cookies, folder_name)
    print(file_paths)
    all_data = []
    for item in file_paths:
        all_data.append(get_file_info(item, cookies, to_html))
    if to_db:
        update_url = sb.get_now_sync()
        print(update_url)
        update_data = [item for item in all_data if item[1] in update_url]
        insert_data = list(set(all_data) - set(update_data))
        # insert
        sb.insert_data(insert_data)
        # update
        sb.update_data(update_data)

    else:
        for item in all_data:
            to_txt(item[0], item[1], item[2])


if __name__ == '__main__':
    save_all(True, True)
