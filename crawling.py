from selenium import webdriver
import time

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(r"C:\Users\pc\Desktop\chromedriver")

url = 'https://oia.yonsei.ac.kr/partner/expReport.asp?ucode=DK000003&bgbn=A'

driver.get(url)

time.sleep(3)

e = driver.find_element_by_class_name('')
print(e.text)

driver.close()


"""
# This one gets all table data text 
import pandas as pd
import requests
from bs4 import BeautifulSoup

res = requests.get("https://oia.yonsei.ac.kr/partner/expReport.asp?ucode=DK000003&bgbn=A")
soup = BeautifulSoup(res.content,'lxml')
table = soup.find_all('table')[0]
df = pd.read_html(str(table),encoding='utf-8')
# print(df[0].to_json(orient='records'))
print(df)
"""
