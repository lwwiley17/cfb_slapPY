# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 11:55:34 2024

@author: wiley
"""

# data magic
import pandas as pd
import numpy as np

gsis = pd.read_csv('gsis_info.csv')
ncaa = pd.read_csv('ncaa_team_code.csv',skiprows=2)

snoop = gsis.merge(ncaa, how = 'outer', left_on='NCAA ID', right_on='ID')

print(snoop.head())
snoop.to_csv('joint.csv', index=False)
