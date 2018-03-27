#import necessary python packages
from urllib2 import urlopen, URLError
from bs4 import BeautifulSoup
import time
import os
import shutil
import requests
from selenium import webdriver

#import web driver file to access chrome via code
driver = webdriver.Chrome('/Users/PMcG/Documents/python packages/chromedriver')

driver.get("http://responsibletechnology.org/gmo-education/")

element = driver.find_element_by_tag_name("p")
Element = driver.find_element_by_class_name("entry-content")

element.get_attribute('text')

text = element.text
Text = Element.text

print Element.text
print element.text



driver.close() #close the driver
