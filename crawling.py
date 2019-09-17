# This one gets all table data text
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import csv




page = 1

dummy_data1 = { }
# 'id': ['1', '2', '3', '4', '5'],
# 'Feature1': ['A', 'C', 'E', 'G', 'I']


df = pd.DataFrame(dummy_data1)

while page:
    univ_query = "DK000003"
    url = "https://oia.yonsei.ac.kr/partner/expReport.asp?page=" + str(page)+"&cur_pack=0&ucode="+str(univ_query)+"&bgbn=A"
    res = requests.get(url)
    soup = BeautifulSoup(res.content,'lxml')
    table = soup.find_all('table')[0]
    # df = pd.read_html(str(table),encoding='utf-8')
    # print(table)
    df_crawl = pd.read_html(str(table),encoding='utf-8', header=0)[0]
    df_crawl['href'] = [np.where(tag.has_attr('href'),tag.get('href'),"no link") for tag in table.find_all('a')]
    # print(df[0].to_json(orient='records')) #this one turns table texts into json
    # print(df) #this one prints mere table texts
    print(df_crawl['href'])
    df_to_save = df_crawl['href']
    # print(df.index)
    if not df_crawl.empty:
        page += 1
        # df1.append(df['href'], ignore_index=True)
        df = pd.concat([df, df_crawl],sort=False)
    else:
        print(df)
        break

df_without_index = df.reset_index()
print(df_without_index)
df_without_index.to_csv(r'C:/Users/pc/Documents/GitHub/OIA_Text_Wrangling/'+univ_query+'.csv',index=False,encoding="utf-8")
