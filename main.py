# 因为知网总是拿caj这种论文格式恶心国人，而pdf版中文论文下起来还得去洋大人用的海外版知网去搜，眼看我的速读100篇论文计划光是这番操作就要浪费不少生命，于是抄起键盘写了这个中文论文下载工具
import requests
import bs4
import webbrowser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import openpyxl

proxies = {
    'https': 'https://127.0.0.1:58591',
    'http': 'http://127.0.0.1:58591'
}
head = {
    'method': 'GET',
    'scheme': 'https',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
}
# as_vis 防止引用出现报错， 自2016年起，测试词 航空发动机 数据融合
url = "https://scholar.google.com/scholar?as_vis=1&as_ylo=2016&q=航空发动机 数据融合"


# url = "https://www.google.com"

# 搜索谷歌某页结果，传入start，以0开始，10为步长
def print_hi(start):
    response = requests.get(url + "&start=" + str(start), proxies=proxies, headers=head)
    # 查看响应状态码
    status_code = response.status_code
    # 使用BeautifulSoup解析代码,并锁定页码指定标签内容
    content = bs4.BeautifulSoup(response.content.decode("utf-8"), "lxml")
    element = content.find_all("div", attrs={"class": "gs_ri"})
    for b_tag in content.findAll('b'):
        b_tag.replace_with(b_tag.contents[0])
    for br_tag in content.findAll('br'):
        br_tag.replace_with('')
    print(status_code)
    title = ''
    author = ''
    abstract = ''
    res = []
    for result in element:
        # 这里有个作者显示不全的问题，.get_text()可能已经解决了此问题
        # for a_tag in result.findAll("div", attrs={"class": "gs_a"}):
        #     # a_tag.replace_with(a_tag.contents[0])
        #     print(a_tag.find("a").contents)

        # print(result)
        # print(result.find("a").contents, result.find("div", attrs={"class": "gs_rs"}).contents)
        # print(title.join(result.find("a").contents), result.find("a")["href"],
        #       result.find("div", attrs={"class": "gs_a"}).contents[0],
        #       abstract.join(result.find("div", attrs={"class": "gs_rs"}).contents))

        epaper = {
            'title': title.join(result.find("a").contents),
            # 'author': author.join(result.find("div", attrs={"class": "gs_a"}).contents),
            'author': result.find("div", attrs={"class": "gs_a"}).get_text(),
            'abstract': abstract.join(result.find("div", attrs={"class": "gs_rs"}).contents),
            'url': result.find("a")["href"]
        }
        res.append(epaper)
    return res


# 进入网站获取完整摘要
def get_abst(url):
    print(url)
    response = requests.get(url, proxies=proxies, headers=head)
    # 查看响应状态码
    status_code = response.status_code
    # 使用BeautifulSoup解析代码,并锁定页码指定标签内容
    content = bs4.BeautifulSoup(response.content.decode("utf-8"), "lxml")
    # TODO 这里需要一个正则匹配摘要
    element = content.find("span", attrs={"id": "ChDivSummary"})
    return element.get_text()


def write_excel_xlsx(path, sheet_name, value):
    index = len(value)
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = sheet_name
    for i in range(0, index):
        for j in range(0, len(value[i])):
            sheet.cell(row=i+1, column=j+1, value=str(value[i][j]))
    workbook.save(path)
    print("xlsx格式表格写入数据成功！")


# 根据名字下载论文
def download_paper(title):
    # browser = webdriver.Chrome()
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    # 开启静默模式
    browser = webdriver.Chrome(options=chrome_options)
    url = "https://eng.oversea.cnki.net/kns55/brief/result.aspx?txt_1_value1="+title+"&txt_1_sel=%E9%A2%98%E5%90%8D&dbPrefix=SCDB&db_opt=%E4" \
          "%B8%AD%E5%9B%BD%E5%AD%A6%E6%9C%AF%E6%96%87%E7%8C%AE%E7%BD%91%E7%BB%9C%E5%87%BA%E7%89%88%E6%80%BB%E5%BA%93" \
          "&db_value=%E4%B8%AD%E5%9B%BD%E6%9C%9F%E5%88%8A%E5%85%A8%E6%96%87%E6%95%B0%E6%8D%AE%E5%BA%93%2C%E4%B8%AD%E5" \
          "%9B%BD%E5%8D%9A%E5%A3%AB%E5%AD%A6%E4%BD%8D%E8%AE%BA%E6%96%87%E5%85%A8%E6%96%87%E6%95%B0%E6%8D%AE%E5%BA%93" \
          "%2C%E4%B8%AD%E5%9B%BD%E4%BC%98%E7%A7%80%E7%A1%95%E5%A3%AB%E5%AD%A6%E4%BD%8D%E8%AE%BA%E6%96%87%E5%85%A8%E6" \
          "%96%87%E6%95%B0%E6%8D%AE%E5%BA%93%2C%E4%B8%AD%E5%9B%BD%E9%87%8D%E8%A6%81%E4%BC%9A%E8%AE%AE%E8%AE%BA%E6%96" \
          "%87%E5%85%A8%E6%96%87%E6%95%B0%E6%8D%AE%E5%BA%93%2C%E5%9B%BD%E9%99%85%E4%BC%9A%E8%AE%AE%E8%AE%BA%E6%96%87" \
          "%E5%85%A8%E6%96%87%E6%95%B0%E6%8D%AE%E5%BA%93%2C%E4%B8%AD%E5%9B%BD%E9%87%8D%E8%A6%81%E6%8A%A5%E7%BA%B8%E5" \
          "%85%A8%E6%96%87%E6%95%B0%E6%8D%AE%E5%BA%93%2C%E4%B8%AD%E5%9B%BD%E5%B9%B4%E9%89%B4%E7%BD%91%E7%BB%9C%E5%87" \
          "%BA%E7%89%88%E6%80%BB%E5%BA%93&search-action=brief%2Fresult.aspx "
    browser.get(url)  # 打开浏览器预设网址
    browser.minimize_window()
    browser.get(
        "https://eng.oversea.cnki.net/kns55/brief/brief.aspx?pagename=ASP.brief_result_aspx&dbPrefix=SCDB&dbCatalog=%e4%b8%ad%e5%9b%bd%e5%ad%a6%e6%9c%af%e6%96%87%e7%8c%ae%e7%bd%91%e7%bb%9c%e5%87%ba%e7%89%88%e6%80%bb%e5%ba%93&ConfigFile=SCDB.xml&research=off&t=1601044487255")
    # print(browser.page_source)  # 打印网页源代码
    content = bs4.BeautifulSoup(browser.page_source, "lxml")
    # print(content)
    firstpaper = content.find("table", attrs={"class": "GridTableContent"}).findAll('tr')[1]
    pmsg = firstpaper.findAll("td")
    # 链接 题目 作者 机构 年份 水平
    dlink = "https://eng.oversea.cnki.net/kns55/brief/" + pmsg[1].contents[0]["href"]
    title = pmsg[2].find('font', attrs={"class": "Mark"}).get_text().replace("\n", "").replace(" ", "")
    url_for_abs = "https://eng.oversea.cnki.net"+pmsg[2].contents[1]['href']
    author = pmsg[3].get_text().replace("\n", "").replace(" ", "")
    institue = pmsg[4].get_text().replace("\n", "").replace(" ", "")
    year = pmsg[5].get_text().replace("\n", "").replace(" ", "")
    ptype = pmsg[6].get_text().replace("\n", "").replace(" ", "")
    print(title, author, institue, year, ptype, url_for_abs)
    new_abst = get_abst(url_for_abs)
    browser.close()  # 关闭浏览器
    return {"dlink": dlink, "title": title, "abst": new_abst}


if __name__ == '__main__':
    # 这里是要查询的谷歌学术页数
    res = print_hi(0)
    # res = res + print_hi(10)
    # res = res + print_hi(20)
    # res = res + print_hi(30)
    # res = res + print_hi(40)
    # res = res + print_hi(50)

    # 命名生成的html
    GEN_HTML = "test.html"
    # 打开文件，准备写入
    f = open(GEN_HTML, 'w', encoding="utf-8")

    # 准备相关变量
    idx = 0
    para = ''
    value_for_xlsx = []
    for paper in res:
        # 获取完整摘要
        # paper['abstract'] = get_abst(paper['url'])
        idx = idx + 1
        dmsg = download_paper(paper['title'])
        para = para + ("<p>标题：<a href='%s'>%s</a> 作者：%s <p>摘要：%s</p><p>%d可下载的标题：<a "
                       "href='%s'>%s</a></p><p>知网摘要：%s</p></p>" % (paper['url'], paper['title'], paper['author'],
                                                                   paper['abstract'], idx, dmsg['dlink'],
                                                                   dmsg['title'], dmsg['abst']))
        value_for_xlsx.append([paper['url'], paper['title'], paper['author'], paper['abstract'], dmsg['dlink'], dmsg['title'], dmsg['abst'], 0])

    book_name_xlsx = 'xlsx格式测试工作簿.xlsx'
    sheet_name_xlsx = 'xlsx格式测试表'
    write_excel_xlsx(book_name_xlsx, sheet_name_xlsx, value_for_xlsx)
    message = """
    <html>
    <head></head>
    <body>
    %s
    </body>
    </html>""" % para

    # 写入文件
    f.write(message)
    # 关闭文件
    f.close()

    # 运行完自动在网页中显示
    webbrowser.open(GEN_HTML, new=1)
