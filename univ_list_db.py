import re
from urllib.request import urlopen
from xlwt import Workbook
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import csv

#HTML tag removal function
def remove_tag(content):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', content)
    return cleantext

def make_con_code_list():
    doc = """
    <option value="AF">AFGHANISTAN</option><option value="AR">ARGENTINA</option><option value="AU">AUSTRALIA</option><option value="AT">AUSTRIA</option><option value="BD">BANGLADESH</option><option value="BE">BELGIUM</option><option value="BR">BRAZIL</option><option value="BN">BRUNEI</option><option value="BG">BULGARIA</option><option value="KH">CAMBODIA</option><option value="CA">CANADA</option><option value="CL">CHILE</option><option value="CN">CHINA</option><option value="CR">COSTA RICA</option><option value="CZ">CZECH REPUBLIC</option><option value="DK">DENMARK</option><option value="EE">ESTONIA</option><option value="FI">FINLAND</option><option value="FR">FRANCE</option><option value="DE">GERMANY</option><option value="GH">GHANA</option><option value="HK">HONG KONG</option><option value="HU">HUNGARY</option><option value="IS">ICELAND</option><option value="IN">INDIA</option><option value="ID">INDONESIA</option><option value="IR">IRAN</option><option value="IE">IRELAND</option><option value="IL">ISRAEL</option><option value="IT">ITALY</option><option value="JP">JAPAN</option><option value="JO">JORDAN</option><option value="KZ">KAZAKHSTAN</option><option value="LV">LATVIA</option><option value="LT">LITHUANIA</option><option value="MY">MALAYSIA</option><option value="MT">MALTA</option><option value="MX">MEXICO</option><option value="MN">MONGOLIA</option><option value="NP">NEPAL</option><option value="NL">NETHERLANDS</option><option value="NZ">NEW ZEALAND</option><option value="NI">NICARAGUA</option><option value="NO">NORWAY</option><option value="PH">PHILIPPINES</option><option value="PL">POLAND</option><option value="PT">PORTUGAL</option><option value="PR">PUERTO RICO</option><option value="RU">RUSSIAN FEDERATION</option><option value="SG">SINGAPORE</option><option value="ZA">SOUTH AFRICA</option><option value="ES">SPAIN</option><option value="SE">SWEDEN</option><option value="CH">SWITZERLAND</option><option value="TW">TAIWAN</option><option value="TH">THAILAND</option><option value="TR">TURKEY</option><option value="GB">UNITED KINGDOM</option><option value="US">UNITED STATES</option><option value="UY">URUGUAY</option><option value="VN">VIETNAM</option><option value="ZW">ZIMBABWE</option>
    """

    #Separating doc HTML
    soup_concod=BeautifulSoup(doc,'lxml')
    list_concod=soup_concod.findAll('option')
    #print(list_concod)

    #Parsing Country Name String List
    soup_con=BeautifulSoup(doc,'lxml')
    list_con= [str(x.text) for x in soup_con.find_all('option')]
    #print(list_con)

    list_con_abv = []
    con_numb=0
    while con_numb < len(list_con) :
        #extracting individual country codes
        item_concod=list_concod[con_numb]
        str_item_concod=str(item_concod)
        code= str_item_concod[15:17]
        list_con_abv.append(code)
        con_numb+=1
    print(list_con_abv)
    return list_con_abv

def make_con_db():
    dummy_data1 = {}
    df = pd.DataFrame(dummy_data1)

    # country_list = make_con_code_list()
    country_list = ['AF', 'AR', 'AU', 'AT', 'BD', 'BE', 'BR', 'BN', 'BG', 'KH', 'CA', 'CL', 'CN', 'CR', 'CZ', 'DK', 'EE', 'FI', 'FR', 'DE', 'GH', 'HK', 'HU', 'IS', 'IN', 'ID', 'IR', 'IE', 'IL', 'IT', 'JP', 'JO', 'KZ', 'LV', 'LT', 'MY', 'MT', 'MX', 'MN', 'NP', 'NL', 'NZ', 'NI', 'NO', 'PH', 'PL', 'PT', 'PR', 'RU', 'SG', 'ZA', 'ES', 'SE', 'CH', 'TW', 'TH', 'TR', 'GB', 'US', 'UY', 'VN', 'ZW']
    # country_list = ['AU','DK','FI']
    for country in country_list:
        url = "https://oia.yonsei.ac.kr/partner/expReport.asp?yn=Y&country_code="+country+"&univ="
        res = requests.get(url)
        soup = BeautifulSoup(res.content,'lxml')
        table = soup.find_all('table')[0]
        df_crawl = pd.read_html(str(table),encoding='utf-8', header=0)[0]
        # print(df_crawl)
        df_crawl['href'] = [np.where(tag.has_attr('href'),tag.get('href'),"no link") for tag in table.find_all('a')]
        print(df_crawl)
        df = pd.concat([df, df_crawl],sort=False)
    df_without_index = df.reset_index()
    print(df_without_index)
    df_without_index.to_csv(r'C:/Users/pc/Documents/GitHub/OIA_Text_Wrangling/univ_db_full.csv',index=False,encoding="utf-8")




