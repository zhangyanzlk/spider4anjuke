"""
使用selenium webdriver进行数据抓取，采用的浏览器为Firefox
"""
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (ElementClickInterceptedException,
                                        ElementNotInteractableException,
                                        ElementNotSelectableException,
                                        ElementNotVisibleException,
                                        ErrorInResponseException,
                                        InsecureCertificateException,
                                        InvalidCoordinatesException,
                                        InvalidElementStateException,
                                        InvalidSessionIdException,
                                        InvalidSelectorException,
                                        ImeNotAvailableException,
                                        ImeActivationFailedException,
                                        InvalidArgumentException,
                                        InvalidCookieDomainException,
                                        JavascriptException,
                                        MoveTargetOutOfBoundsException,
                                        NoSuchCookieException,
                                        NoSuchElementException,
                                        NoSuchFrameException,
                                        NoSuchWindowException,
                                        NoAlertPresentException,
                                        ScreenshotException,
                                        SessionNotCreatedException,
                                        StaleElementReferenceException,
                                        TimeoutException,
                                        UnableToSetCookieException,
                                        UnexpectedAlertPresentException,
                                        UnknownMethodException,
                                        WebDriverException)
import re
from lxml import etree
import time
from time import sleep
import random
import csv
import json

headers_zh = ['名称', '地址', '纬度', '经度', '本月均价', '物业类型', '物业费', '总建筑面积', '总户数', '建造年代',
              '停车位', '容积率', '绿化率', '开发商', '物业公司', '相关学校', '出售房源', '出租房源', '地区价格', '小区价格']
headers_en = ['name', 'address', 'lat', 'lng', 'average', 'style', 'property_costs', 'total_area', 'households', 'age',
              'park', 'volume_ratio', 'green_ratio', 'developer', 'property', 'school', 'for_sales', 'for_rent', 'area_price', 'community_price']
receive_data = {
    'name': '',
    'address': '',
    'lat': '',
    'lng': '',
    'average': '',
    'style': '',
    'property_costs': '',
    'total_area': '',
    'households': '',
    'age': '',
    'park': '',
    'volume_ratio': '',
    'green_ratio': '',
    'developer': '',
    'property': '',
    'school': '',
    'for_sales': '',
    'for_rent': '',
    'area_price': '',
    'community_price': ''
}

def get_price_trend(price):
    str = '{'
    for i in price:
        for key in i:
            str += ' '
            str += i[key]
    str += ' }'
    return str

# 浏览器窗口句柄索引
hdl_index = 0
# 打开浏览器
# browser = webdriver.Firefox(executable_path = "E:\Python\Python36\webdrivers\geckodriver")
browser = webdriver.Chrome(executable_path = "E:\Python\Python36\webdrivers\chromedriver")
# 创建动作链
actionchain = ActionChains(browser)
# 设置隐式时间等待
browser.implicitly_wait(10)
wait = WebDriverWait(browser, 10)

with open("anjuk_data.csv", "a+", newline='') as aj_data:
    norm_writer = csv.writer(aj_data)
    dic_writer = csv.DictWriter(aj_data, headers_en)
    dic_writer.writeheader()

    browser.get("https://chongqing.anjuke.com/community/yubei/o4-y2/")
    while True:
        try:
            lst = browser.find_elements_by_xpath("//*[@class='list-content']/*[@class='li-itemmod']")
        except Exception as e:
            print("Exception found", format(e))

        for lst_i in lst:
            browser.execute_script("arguments[0].scrollIntoView();", lst_i)
            lst_i.click()
            hdl_index += 1
            browser.switch_to.window(browser.window_handles[hdl_index])

            wait.until(EC.presence_of_element_located(
                (By.XPATH, "//script[@type='text/javascript' and not(@src) and contains(./text(), 'lat :')]")))
            doc = browser.page_source
            dom_tree = etree.HTML(doc)
            # receive_data['lat'] = re.search(r'[0-9\.]+', re.search(r'lat : \"[0-9\.]+\"', doc).group()).group()
            # receive_data['lng'] = re.search(r'[0-9\.]+', re.search(r'lng : \"[0-9\.]+\"', doc).group()).group()
            temp = re.search(r'var MapOps = ({[\S\s]+?}\n)', doc, re.S).group(1)
            receive_data['name'] = re.search(r'name : \"(.+?)\"', temp).group(1)
            receive_data['lat'] = re.search(r'lat : \"(.+?)\"', temp).group(1)
            receive_data['lng'] = re.search(r'lng : \"(.+?)\"', temp).group(1)
            receive_data['address'] = browser.find_element_by_xpath("//div[@class = 'comm-title']/h1/span").text
            receive_data['average'] = browser.find_element_by_xpath("//div[@id = 'basic-infos-box']/div/span[@class = 'average']").text.strip('元/m²')
            receive_data['style'] = browser.find_element_by_xpath("//dl[@class = 'basic-parms-mod']/dd[1]").text
            receive_data['property_costs'] = browser.find_element_by_xpath("//dl[@class = 'basic-parms-mod']/dd[2]").text.replace('㎡', '平米').replace('m²', '平米')
            receive_data['total_area'] = browser.find_element_by_xpath("//dl[@class = 'basic-parms-mod']/dd[3]").text.replace('m²', '平米')
            receive_data['households'] = browser.find_element_by_xpath("//dl[@class = 'basic-parms-mod']/dd[4]").text
            receive_data['age'] = browser.find_element_by_xpath("//dl[@class = 'basic-parms-mod']/dd[5]").text
            receive_data['park'] = browser.find_element_by_xpath("//dl[@class = 'basic-parms-mod']/dd[6]").text
            receive_data['volume_ratio'] = browser.find_element_by_xpath("//dl[@class = 'basic-parms-mod']/dd[7]").text
            receive_data['green_ratio'] = browser.find_element_by_xpath("//dl[@class = 'basic-parms-mod']/dd[8]").text
            receive_data['developer'] = browser.find_element_by_xpath("//dl[@class = 'basic-parms-mod']/dd[9]").text
            receive_data['property'] = browser.find_element_by_xpath("//dl[@class = 'basic-parms-mod']/dd[10]").text
            if len(dom_tree.xpath("//dl[@class = 'basic-parms-mod']/dd[11]")):
                try:
                    receive_data['school'] = browser.find_element_by_xpath("//dl[@class = 'basic-parms-mod']/dd[11]").text
                except NoSuchElementException:
                    receive_data['school'] = ''
            receive_data['for_sales'] = browser.find_element_by_xpath("//div[@class = 'houses-sets-mod j-house-num']/a[@data-soj = 'baseinfopro']").text.strip('套')
            receive_data['for_rent'] = browser.find_element_by_xpath("//div[@class = 'houses-sets-mod j-house-num']/a[@data-soj = 'baseinfopro']").text.strip('套')
            temp = re.search(r'}else{\n.+ajk.chart.priceTrend\(({[\S\s]+?})\);', doc, re.S).group(1)
            temp = re.search(r'data : ({.+?}),\n', temp, re.S).group(1)
            temp = json.loads(temp)
            receive_data['area_price'] = get_price_trend(temp['area'])
            receive_data['community_price'] = get_price_trend(temp['community'])

            dic_writer.writerow(receive_data)

            time.sleep(random.randrange(3, 10, 1))
            # circle = wait.until(EC.presence_of_element_located((
            #     By.XPATH, "//*[@id='linechart']/*[name()='svg']/*[name()='circle'][1]")))
            # circle = browser.find_element_by_xpath("//*[@id='linechart']/svg/circle[1]")
            # circle = browser.find_element_by_xpath("//*[@id='linechart']/*[name()='svg']/*[name()='circle'][1]")
            # ActionChains(browser).move_to_element(circle).perform()
            # 关闭当前窗口
            browser.close()
            hdl_index -= 1
            browser.switch_to.window(browser.window_handles[hdl_index])

        try:
            wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[@class='multi-page']/a[contains(text(), '下一页') and @href]"))).click()
        except TimeoutException:
            break

# 关闭所有窗口
browser.quit()
