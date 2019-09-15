# This one gets all table data text
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

page = 1
while page < 10:
    univ_query = "DK000003"
    url = "https://oia.yonsei.ac.kr/partner/expReport.asp?page=" + str(page)+"&cur_pack=0&ucode="+str(univ_query)+"&bgbn=A"
    res = requests.get(url)
    soup = BeautifulSoup(res.content,'lxml')
    table = soup.find_all('table')[0]
    # df = pd.read_html(str(table),encoding='utf-8')
    # print(table)
    df = pd.read_html(str(table),encoding='utf-8', header=0)[0]
    df['href'] = [np.where(tag.has_attr('href'),tag.get('href'),"no link") for tag in table.find_all('a')]
    # print(df[0].to_json(orient='records')) #this one turns table texts into json
    # print(df) #this one prints mere table texts
    print(df['href'])
    # print(df.index)
    if not df.empty:
        page += 1
    else:
        break

