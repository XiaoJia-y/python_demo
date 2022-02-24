# -*- encoding=utf-8 -*-
from ast import Global
from email import header
from lib2to3.pgen2 import driver
import MySQLdb
import logging
from bs4 import BeautifulSoup
import logging
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import time
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--headless')


class Get_data(object):
    #打开网页
    def gethtml(self, place, driver):
        try:
            headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
        }
            driver.get('http://vacations.ctrip.com/')
            search = driver.find_element_by_class_name('search_txt')
            search.click()
            check = driver.find_element_by_class_name('main_search_btn')
            search.send_keys(place)
            check.click()
            return driver.page_source
        except TimeoutException:
            logging.error("超时了!")
            self.gethtml(place)

    #换页
    def changepage(self, page, driver):
        try:
            js="var q=document.documentElement.scrollTop=10000"
            driver.execute_script(js)
            time.sleep(5)
            #p =  WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#ipt_page_txt')))
            submit = driver.find_element_by_class_name('down')
            #p.clear()
            submit.click()
            return driver.page_source
        except:
            return self.changepage(page)

    #解析页面
    def checkpage(self, html, datas):
        soup = BeautifulSoup(html,'lxml')
        links = soup.find_all('div',class_='list_product_box js_product_item')
        for link in links:
            data = []
            name = link.find('span',class_='').get_text()
            data.append(name)
            num = link.get("data-track-product-id")
            href="https://vacations.ctrip.com/travel/detail/p{0}/?city=32".format(num)
            data.append(href)
            price = link.find('div',class_='list_sr_price').get_text()
            data.append(price)
            try:
                agree =  link.find('p',class_='list_change_grade').get_text()
            except:
                agree = ''
            try:    
                people = link.find('div',class_='list_change_one').get_text()
                about = link.find('div',class_='list_change_two').get_text()
            except:
                people = ''
                about = ''
            if people == '' and about != '':
                people = about
                about = ''
            data.append(agree)
            data.append(people)
            data.append(about)  
            datas.append(data)
        return datas


    #主函数
    def main(self, place, num):
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.maximize_window()
        datas = []
        html = self.gethtml(place, driver)
        for i in range(2,num):
            html = self.changepage(i, driver)
        data = self.checkpage(html, datas)
        driver.quit()
        data.sort(key=lambda x:x[2])
        return data

if __name__ == '__main__':
    place = input('请输入要查询的地点：')
    G = Get_data()
    num = 3
    data = G.main(place, num)
    # conn = MySQLdb.Connect(host = "42.193.255.161", port = 3306, user = 'root', passwd = '123456', db = 'trip', charset="utf8")
    # s.insert_data(conn, data)