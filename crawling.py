# This one gets all table data text
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import csv



def crwl_as_csv(univ_query):
    page = 1
    dummy_data1 = {}
    df = pd.DataFrame(dummy_data1)
    while page:
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


review_url = "https://oia.yonsei.ac.kr" + "/partner/expReport.asp?id=15129&page=1&bgbn=R"

options = webdriver.ChromeOptions()
# options.add_argument('headless')
driver = webdriver.Chrome(r"C:\Users\pc\Desktop\chromedriver")
driver.implicitly_wait(2) # waiting web source for three seconds implicitly
driver.get(review_url)

body_cursor_list = driver.find_elements_by_class_name("exp_txt")
# print(body_cursor_list)

text_list = []
for i in body_cursor_list:
    text_list.append(i.text)


print("교환대학의 크기, 지리적 위치, 기후 등")
print(text_list[1])
print("대학 주변 환경")
print(text_list[2])
print("거주 형태, 식사")
print(text_list[3])
print("수업, 도서관")
print(text_list[4])
print("국제교육부")
print(text_list[5])
print("기타 학교에 관한 정보(부대시설, 동아리 등)")
print(text_list[6])
print("Culture Shock")
print(text_list[7])
print("도움 받을 수 있는 곳(교내외)")
print(text_list[8])
print("기타")
print(text_list[9])

# print(text_list)
