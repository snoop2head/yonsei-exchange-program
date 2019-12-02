import pandas as pd
from pandas.api.types import CategoricalDtype # 그래프의 값을 정렬해서 보기위해
import numpy as np
from plotnine import *
from konlpy.tag import Mecab

print(pd.__version__)
print(np.__version__)

df = pd.read_csv(r'C:/Users/pc/Documents/GitHub/OIA_Text_Wrangling/DK000003.csv_text_data.csv')

print(df.shape)


basic_info_df = df['gen_info']
print(basic_info_df)

df.columns
df.info()

mecab = Mecab()
text = u"""이제 구글 코랩에서 Mecab-ko라이브러리 사용이 가능합니다. 읽어주셔서 감사합니다."""
nouns = mecab.nouns(text)
nouns
