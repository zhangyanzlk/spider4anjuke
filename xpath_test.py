from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from time import sleep
import re
from lxml import etree

# 浏览器窗口句柄索引
hdl_index = 0

# 打开火狐浏览器
browser = webdriver.Firefox(executable_path = "E:\Python\Python36\webdrivers\geckodriver")
# 创建动作链
actionchain = ActionChains(browser)
# 设置隐式时间等待
browser.implicitly_wait(8)

browser.get("file:///G:/projects/python/spider4anjuke/xpath_test.html")

doc = browser.page_source
dom_tree = etree.HTML(doc)

links = dom_tree.xpath("//*[@id='linechart']/svg/circle[1]")
circle = browser.find_element_by_xpath("//div[@id='linechart']/*[@version='1.1']")
circle = browser.find_element_by_xpath("//div[@id='linechart']/*[@version='1.1']").find_elements_by_tag_name("circle")[1]
circle = browser.find_element_by_xpath("//*[@id='linechart']/*[name()='svg']/*[name()='circle'][1]")

# 关闭当前窗口
# browser.close()

# 关闭所有窗口
# browser.quit()
