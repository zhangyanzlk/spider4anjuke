"""
使用selenium webdriver进行数据抓取，采用的浏览器为Firefox
"""
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import re
import time
from time import sleep
import random

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

browser.get("https://chongqing.anjuke.com/community/yubei/o4-y2/")
try:
    lst = browser.find_elements_by_xpath("//*[@class='list-content']/*[@class='li-itemmod']")
except Exception as e:
    print("Exception found", format(e))

lst[10].click()
hdl_index += 1
browser.switch_to.window(browser.window_handles[hdl_index])
wait.until(EC.presence_of_element_located((By.XPATH, "//script[@type='text/javascript' and not(@src) and contains(./text(), 'lat :')]")))
doc = browser.page_source
lat = re.search(r'[0-9\.]+', re.search(r'lat : \"[0-9\.]+\"', doc).group()).group()
lng = re.search(r'[0-9\.]+', re.search(r'lng : \"[0-9\.]+\"', doc).group()).group()
# 切换到最近3年数据
data_range = browser.find_element_by_xpath("//*[@class='chartTimeTab']/a[3]")
# browser.execute_script("arguments[0].focus();", data_range)
browser.execute_script("arguments[0].scrollIntoView();", data_range)
data_range.click()
# actionchain.move_to_element(data_range).click(data_range).perform()
# ActionChains(browser).move_to_element(data_range).click(data_range).perform()

time.sleep(6)
circle = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='linechart']/*[name()='svg']/*[name()='circle'][1]")))
# circle = browser.find_element_by_xpath("//*[@id='linechart']/svg/circle[1]")
# circle = browser.find_element_by_xpath("//*[@id='linechart']/*[name()='svg']/*[name()='circle'][1]")
ActionChains(browser).move_to_element(circle).perform()
# 关闭当前窗口
# browser.close()

# 关闭所有窗口
# browser.quit()
