# This one gets all table data text
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import csv
from urllib.parse import urlparse


df = pd.read_csv('_department.csv')
result = df.transpose()
result.to_csv(r'C:/Users/pc/Documents/GitHub/OIA_Text_Wrangling/_department_t.csv',index=False,encoding="utf-8")
