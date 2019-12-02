    #-*- coding:utf-8 -*-

import pandas as pd
from soynlp.tokenizer import RegexTokenizer
tokenizer = RegexTokenizer()
import numpy as np
import re


df = pd.read_csv(r'C:/Users/pc/Documents/GitHub/OIA_Text_Wrangling/DK000003.csv_text_data.csv')

print(df.shape)

# print(df.tail)

basic_info_df = df['gen_info']
# print(basic_info_df)


sample_index = 24
sample_content =basic_info_df[sample_index]

# print(sample_content)
tokenized_content = tokenizer.tokenize(sample_content)
print(tokenized_content)


