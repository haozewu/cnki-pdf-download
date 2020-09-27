from urllib import request

import openpyxl
import os
import time
import shutil
from dask.bytes.tests.test_http import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# 这里自己定义浏览器默认下载的地址，这里我定义的是chrome的默认路径
folder_path = "C:\\Users\\haoze\\Downloads\\"

chrome_options = Options()
# chrome_options.add_argument('--headless')
# 开启静默模式
browser = webdriver.Chrome(options=chrome_options)


def get_file_list(file_path):
    dir_list = os.listdir(file_path)
    if not dir_list:
        return
    else:
        # 注意，这里使用lambda表达式，将文件按照最后修改时间顺序升序排列
        # os.path.getmtime() 函数是获取文件最后修改时间
        # os.path.getctime() 函数是获取文件最后创建时间
        dir_list = sorted(dir_list, key=lambda x: os.path.getmtime(os.path.join(file_path, x)))
        # print(dir_list)
        return dir_list


def download_save(param, url):
    if not os.path.exists(folder_path):
        print("Selected folder not exist, try to create it.")
        os.makedirs(folder_path)

    filepath = folder_path + '/' + param['filename'] + ".pdf"
    if os.path.exists(filepath):
        print("File have already exist. skip")
    else:
        try:
            print("Try downloading file: {}".format(url))
            # 这里不设置filepath，后续改名
            # requests.post(url="https://login.cnki.net/login/", data={"__EVENTTARGET": "Button2"})
            # browser.get("https://eng.oversea.cnki.net/kns55/")
            # request.urlretrieve(url, filename=filepath)
            browser.get(url)
        except Exception as e:
            print("Error occurred when downloading file, error message:")
            print(e)
    return 0


def read_excel_xlsx(path, sheet_name):
    workbook = openpyxl.load_workbook(path)
    # sheet = wb.get_sheet_by_name(sheet_name)这种方式已经弃用，不建议使用
    sheet = workbook[sheet_name]
    for row in sheet.rows:
        # print(row[1].value, row[2].value, row[4].value, row[7].value)
        print(row[1].value, row[7].value)
        if row[7].value == 1:
            param = {
                "filename": row[1].value
            }
            download_save(param, row[4].value)
            # 不是因为太快了，而是因为没有采用IP登录，使用浏览器下载规避登录问题
            # 时间设置根据网络判断，否则可能会出现命名错误问题
            time.sleep(60)
            # 这里给文件降序排列改个名
            dir_list = get_file_list(folder_path)
            # 在这里进行文件转移和更名
            try:
                shutil.move(os.path.join(folder_path, dir_list[len(dir_list) - 1]), "./paper/" + row[1].value + ".pdf")
            except:
                pass


if __name__ == '__main__':
    book_name_xlsx = 'xlsx格式测试工作簿.xlsx'
    sheet_name_xlsx = 'xlsx格式测试表'

    read_excel_xlsx(book_name_xlsx, sheet_name_xlsx)
    browser.close()
