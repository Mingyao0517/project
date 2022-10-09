# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 16:22:56 2019

@author: zmy
"""

import pandas as pd
import numpy as np

data = pd.read_csv('data/data.csv')
np_data = data.values
print(np_data)
y = np_data[:,-1]
x = np_data[:,0:-1]

print(x)
print(y)


