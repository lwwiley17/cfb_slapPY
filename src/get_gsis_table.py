# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 10:09:40 2024

@author: wiley
"""

# data magic
import pandas as pd
import numpy as np

# webscraping
import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz

# slow things down
import time

url = 'https://www.nflgsis.com/gsis/documentation/Partners/Schools.htm'

again = True
one = 1

while again:
    print(one)
    one = one + 1
    try:
        dfs = pd.read_html(url)
        again = False
    except:
        pass
    time.sleep(5)

print(len(dfs))

print(dfs[0].head())

dfs[0].to_csv('gsis_info.csv', index=False)