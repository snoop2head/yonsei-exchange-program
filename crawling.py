# This one gets all table data text
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

res = requests.get("https://oia.yonsei.ac.kr/partner/expReport.asp?ucode=DK000003&bgbn=A")
soup = BeautifulSoup(res.content,'lxml')
table = soup.find_all('table')[0]
# df = pd.read_html(str(table),encoding='utf-8')
# print(table)
df = pd.read_html(str(table),encoding='utf-8', header=0)[0]
df['href'] = [np.where(tag.has_attr('href'),tag.get('href'),"no link") for tag in table.find_all('a')]
# print(df[0].to_json(orient='records')) #this one turns table texts into json
# print(df) #this one prints mere table texts
print(df['href'])

