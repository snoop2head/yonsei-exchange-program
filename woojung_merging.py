import os
import json
import re

import pandas as pd
import numpy as np



# 상위 폴더로부터 하위 디렉토리 리스트로 뽑아주는 함수
def load_directory_data(pwd):
    file_path_list = []

    # 디렉토리, 디렉토리 내 폴더 리스트, 파일 리스트
    for path,dirs,files in os.walk(pwd):

        for f in files:
            file_path = path + '/' +f
            file_path_list.append(file_path)

    print(len(file_path_list))
    return file_path_list

FILE_1 = load_directory_data("_JSON 1 Instagram JSON File")
print(FILE_1[:5])
print()
FILE_2 = load_directory_data("_JSON 2 Image OCR Result CSV File")
print(FILE_2[:5])


def read_json(FILE_PATH):

    # read json
    with open(FILE_PATH, encoding='UTF8') as json_file:
        json_data = json.load(json_file)

    user_name = os.path.basename(FILE_PATH)[:-5]
    insta_df = pd.DataFrame()

    for d in json_data:
        hashtag_list = []
        caption_txt = ''
        insta = pd.DataFrame()

        # caption 해시태그 가져오기
        if 'caption' in d:
            # 간단한 전처리
            caption_txt = d['caption'].replace('\n',' ')
            if caption_txt[0] == '-':
                caption_txt = caption_txt[1:]
            caption_txt = caption_txt.strip()
            hashtag_list = re.findall(r"#(\w+)", caption_txt)

        # 기존 코드는 caption이 없을 경우 작동 못함
        # comments에서 해시태그 가져오기
        if 'comments' in d:
            comments = d['comments']
            for c in list(d['comments']):
                # 댓글 작성자가 인스타 유저라면 코멘트 가져오기
                if c['author'] == userName:
                    comment_txt = c['comment']
                    hashtag_list = re.findall(r"#(\w+)", comment_txt)
                    #태그가 저장이 되었다면 for 문 종료
                    if len(hashtag_list) != 0:
                        break

        # 매 loop마다 데이터 쌓기
        insta = pd.DataFrame({'USER_ID': user_name,
                              'CONTENT_ID': d['key'].split('/')[-2],
                              'Content_txt': caption_txt,
                              'Hashtags' : [hashtag_list]})
        insta_df = insta_df.append(insta)
        insta_df = insta_df.reset_index(drop=True)

    return insta_df


def read_csv(FILE_PATH):
    data = pd.read_csv(FILE_PATH,encoding = 'utf-8' )
    data = data.iloc[:,:2]
    data.columns = ['CONTENT_IMAGE_ID','Image_Content_txt']
    # 게시글 아이디
    data['CONTENT_IMAGE_ID'] = data['CONTENT_IMAGE_ID'].apply(lambda x : x[:-4])
    # 게시글에 여러장 있을 경우 추가 구분
    data['CONTENT_ID'] =  data['CONTENT_IMAGE_ID'].apply(lambda x : x[:-2])
    data['USER_ID'] = os.path.basename(FILE_PATH)[:-4]
    data = data[['USER_ID','CONTENT_ID','CONTENT_IMAGE_ID','Image_Content_txt']]

    return data


def merging(FILE_LIST1,FILE_LIST2):
    total_data = 0
    for f_json in FILE_LIST1:
        user_json = os.path.basename(f_json)[:-5]
        insta_data = read_json(f_json)
        for f_csv in FILE_LIST2:
            user_csv = os.path.basename(f_csv)[:-4]
            # 유저 같다면
            if user_json == user_csv:
                ocr_data = read_csv(f_csv)
                print(user_csv)
                merge_df = pd.merge(insta_data,ocr_data,on=['USER_ID','CONTENT_ID'],how='inner')
                merge_df = merge_df[['USER_ID','CONTENT_ID','CONTENT_IMAGE_ID','Image_Content_txt','Content_txt','Hashtags']]
                merge_df.to_csv('Final_Data/' + user_json + '.csv', encoding='utf-8-sig')
                total_data += len(merge_df)
    print("총 데이터 개수",total_data)
merging(FILE_1,FILE_2)


FILE_Final = load_directory_data("Final_Data")
total_df = pd.DataFrame()

for f in FILE_Final:
    df =pd.read_csv(f,encoding = 'utf-8')
    df = df.iloc[:,1:]
    total_df = total_df.append(df,sort=True)

total_df = total_df.iloc[:,:-1]
total_df = total_df[['USER_ID','CONTENT_ID', 'CONTENT_IMAGE_ID','Image_Content_txt','Content_txt', 'Hashtags']]
total_df = total_df.sort_values(['USER_ID','CONTENT_ID','CONTENT_IMAGE_ID'])
total_df = total_df.reset_index(drop = True)
total_df.head()

#total_df.to_csv("Total_Final_Data_v1.csv",encoding='utf-8-sig')


Total_df_v2 = pd.groupby(total_df[['USER_ID','CONTENT_ID','Image_Content_txt','Content_txt','Hashtags']],
           ['USER_ID','CONTENT_ID']).sum().reset_index(drop=False)

Total_df_v2 = Total_df_v2.sort_values(['USER_ID','CONTENT_ID'])
Total_df_v2 = Total_df_v2.reset_index(drop = True)
Total_df_v2.head()


#Total_df_v2.to_csv("Total_Final_Data_v2_concatTxt.csv",encoding='utf-8-sig')


