# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 09:32:28 2019

@author: zmy
"""
import re
s = "<FileStorage: 'data.csv' ('application/vnd.ms-excel')>)])>"
filename = re.findall(r'\'.*?.csv\'',s)
