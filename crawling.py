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
        # print(df_crawl['href'])
        # df_to_save = df_crawl['href'] # these are only href parts
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

# crwl_as_csv("DK000003")


def input_text(href):
    empty_lst = []
    review_url = "https://oia.yonsei.ac.kr" + href

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(r"C:\Users\pc\Desktop\chromedriver", options=options)
    driver.implicitly_wait(2) # waiting web source for three seconds implicitly
    driver.get(review_url)

    # selenium body cursor list
    body_cursor_list = driver.find_elements_by_class_name("exp_txt")
    # print(body_cursor_list)

    text_list = []
    for i in body_cursor_list:
        text_list.append(i.text)

    text_list = text_list[1:]
    """
    # print("교환대학의 크기, 지리적 위치, 기후 등")
    # print(text_list[1])
    gen_info = text_list[1]
    # print("대학 주변 환경")
    # print(text_list[2])
    env_info  = text_list[2]
    # print("거주 형태, 식사")
    # print(text_list[3])
    food_info = text_list[3]
    # print("수업, 도서관")
    # print(text_list[4])
    study_info = text_list[4]
    # print("국제교육부")
    # print(text_list[5])
    office_info = text_list[5]
    # print("기타 학교에 관한 정보(부대시설, 동아리 등)")
    # print(text_list[6])
    facil_info = text_list[6]
    # print("Culture Shock")
    # print(text_list[7])
    mhct_info = text_list[7]
    # print("도움 받을 수 있는 곳(교내외)")
    # print(text_list[8])
    help_info = text_list[8]
    # print("기타")
    # print(text_list[9])
    etc_info = text_list[9]
    # print(text_list)
    single_dict = {
        "교환대학의 크기, 지리적 위치, 기후 등": gen_info,
        "대학 주변 환경": env_info,
        "거주 형태, 식사": food_info,
        "수업, 도서관": study_info,
        "국제교육부": office_info,
        "기타 학교에 관한 정보(부대시설, 동아리 등)": facil_info,
        "Culture Shock": mhct_info,
        "도움 받을 수 있는 곳(교내외)": help_info,
        "기타": etc_info}

    single_list = [gen_info, env_info, food_info, study_info, office_info, facil_info, mhct_info, help_info, etc_info]
    # df1 = pd.DataFrame(single_dict, columns = ['교환대학의 크기, 지리적 위치, 기후 등','대학 주변 환경','거주 형태, 식사',
    #                                            '수업, 도서관', '국제교육부', '기타 학교에 관한 정보(부대시설, 동아리 등)',
    #                                            'Culture Shock', '도움 받을 수 있는 곳(교내외)','기타'])
    # print(df1)
    # df1.to_csv(r'C:/Users/pc/Documents/GitHub/OIA_Text_Wrangling/'+"UoC_sample_1"+'.csv',index=False,encoding="utf-8")
    empty_lst.append(single_dict)
    print(single_dict)
    df = pd.DataFrame.from_dict(single_dict, orient="index")
    """
    return text_list



# input_text("/partner/expReport.asp?id=15129&page=1&bgbn=R")


"""
single_dict = {
    "gen_info": [1],
    "env_info": [2],
    "food_info": [3],
    "study_info": [4],
    "office_info": [5],
    "facil_info": [6],
    "mhct_info": [7],
    "help_info": [8],
    "etc_info": [9]}

df = pd.DataFrame(single_dict, index = [1,2,3,4,5,6,7,8,9])

print(df.head())
"""

def combining_into_csv(file_name):
    initial_df = pd.read_csv(file_name)
    stacked_list = []
    for item in initial_df['href']:
        print(item)
        text_list = input_text(item)
        stacked_list.append(text_list)
    univ_text_df= pd.DataFrame(np.column_stack(stacked_list),
                               columns=["gen_info", "env_info", "food_info", "study_info", "office_info", "facil_info", "mhct_info","help_info","etc_info"])
    print(univ_text_df)
    univ_text_df.to_csv(r'C:/Users/pc/Documents/GitHub/OIA_Text_Wrangling/'+"2"+'.csv',index=False,encoding="utf-8")


    """
        new_df = input_text(item)
        base_df = pd.concat([base_df,new_df], axis=1)
    print(base_df)
    base_df.to_csv(r'C:/Users/pc/Documents/GitHub/OIA_Text_Wrangling/'+"1"+'.csv',index=False,encoding="utf-8")
    """


combining_into_csv("DK000003.csv")

"""
for index, row in df.iterrows():
    print(row['href'])
"""

