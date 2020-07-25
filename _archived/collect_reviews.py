# This one gets all table data text
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import csv
from urllib.parse import urlparse

def crwl_as_csv(univ_query):
    page = 1
    dummy_data1 = {}
    df = pd.DataFrame(dummy_data1)
    while page:
        url = "https://oia.yonsei.ac.kr/partner/expReport.asp?page=" + str(page)+"&cur_pack=0&ucode="+str(univ_query)+"&bgbn=A"
        res = requests.get(url)
        soup = BeautifulSoup(res.content,'lxml')
        table = soup.find_all('table')[0]
        df_crawl = pd.read_html(str(table),encoding='utf-8', header=0)[0]
        df_crawl['href'] = [np.where(tag.has_attr('href'),tag.get('href'),"no link") for tag in table.find_all('a')]
        if not df_crawl.empty:
            page += 1
            df = pd.concat([df, df_crawl],sort=False)
        else:
            print(df)
            break
    df_without_index = df.reset_index()
    print(df_without_index)
    df_without_index.to_csv(r'/Users/noopy/Yonsei_Exchange_Text_Wrangling/'+univ_query+'.csv',index=False,encoding="utf-8")


def input_text(href):
    empty_lst = []
    review_url = "https://oia.yonsei.ac.kr" + href
    res = requests.get(review_url)
    soup = BeautifulSoup(res.content,'lxml')
    body_cursor_list = soup.find_all("div", {"class": "exp_txt"})
    # options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    # driver = webdriver.Chrome(r"C:\Users\pc\Desktop\chromedriver", options=options)
    # driver.implicitly_wait(1) # waiting web source for one second implicitly
    # driver.get(review_url)

    # selenium body cursor list
    # body_cursor_list = driver.find_elements_by_class_name("exp_txt")

    text_list = []
    for i in body_cursor_list:
        text_list.append(i.text)

    text_list = text_list[1:]
    return text_list

# input_text("/partner/expReport.asp?id=15129&page=1&bgbn=R")


def combining_into_csv(file_name):
    initial_df = pd.read_csv(r'C:/Users/pc/Documents/GitHub/OIA_Text_Wrangling/dataf/'+file_name)
    stacked_list = []
    for item in initial_df['href']:
        print(item)
        text_list = input_text(item)
        stacked_list.append(text_list)
    univ_text_df= pd.DataFrame(np.row_stack(stacked_list),
                               columns=["gen_info", "env_info", "food_info", "study_info", "office_info", "facil_info", "mhct_info","help_info","etc_info"])
    print(univ_text_df)
    univ_text_df.to_csv(r'C:/Users/pc/Documents/GitHub/OIA_Text_Wrangling/dataf/'+file_name+'_text_data.csv',index=False,encoding="utf-8")

def make_file(university_query):
    crwl_as_csv(university_query)
    file_name = university_query + ".csv"
    combining_into_csv(file_name)


def give_cde_from_url(href):
    query =urlparse(href)
    query_list = query.query.split('=')
    query_list2 = query_list[1].split('&')
    univ_code = query_list2[0]
    print(univ_code)
    return univ_code

def mke_csv_files():
    df = pd.read_csv('univ_db_final_cont.csv')
    for href in df['href']:
        univ_code = give_cde_from_url(href)
        crwl_as_csv(univ_code)
        file_name = univ_code + ".csv"
        combining_into_csv(file_name)

mke_csv_files()
