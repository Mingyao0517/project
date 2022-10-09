# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 22:00:32 2019

@author: zmy
"""

#from sklearn import preprocessing
#import numpy as np
#x = np.array([
#[ 1., -1.,  2.],
#[ 2.,  0.,  0.],
#[ 0.,  1., -1.]])
#print('原始数据为：\n',x)
##
##print('method1:指定均值方差数据标准化(默认均值0 方差 1):')
##print('使用scale()函数 按列标准化')
##x_scaled = preprocessing.scale(x)
##print('标准化后矩阵为:\n',x_scaled,end='\n\n')
##print('cur mean:', x_scaled.mean(axis=0), 'cur std:', x_scaled.std(axis=0))
#
#print('使用scale()函数 按行标准化')
#x_scaled = preprocessing.scale(x,axis=1)
#print('标准化后矩阵为:\n',x_scaled,end='\n')
#print('cur mean:', x_scaled.mean(axis=1), 'cur std:', x_scaled.std(axis=1))
#print('\nmethod2:StandardScaler类,可以保存训练集中的参数')
#scaler = preprocessing.StandardScaler().fit(x)
#print('标准化前 均值方差为:',scaler.mean_,scaler.scale_)
#print('标准化后矩阵为:\n',scaler.transform(x),end='\n\n')
import numpy as np
from sklearn import datasets,linear_model,preprocessing

# 定义训练数据
#x = np.array([[100,4,9.3],[50,3,4.8],[100,4,8.9],
#              [100,2,6.5],[50,2,4.2],[80,2,6.2],
#              [75,3,7.4],[65,4,6],[90,3,7.6],[90,2,6.1]])
x = np.array([[24.7849,13.5036,15.6111,31.2494],           #数据格式因该是 横向 x1 x2 ，，，，
              [56.6593,86.7704,93.3127,69.8421],
              [55.8005,88.6280,68.9021,113.7907],
              [65.0791,88.3041,91.5868,80.6926],
              [125.9283,135.0274,140.6267,139.9881],
              [112.5840,126.0310,112.6886,157.5936],
              [41.4236,36.8813,26.0484,56.7237],
              [32.9571,37.6037,26.9444,50.7283]])

y = np.array([21.2872,73.1462,81.7803,81.4157,135.3701,127.2243,40.2691,37.3084])
print(x)
X = x[:,:]
Y = y[:]
print(X,Y)

# 训练数据
regr = linear_model.LinearRegression()
regr.fit(X,Y)

print('coefficients(b1,b2...):',regr.coef_)
print('intercept(b0):',regr.intercept_)
##########求标准差  按列求
print("按列求标准差################")
#x_scaled = preprocessing.scale(X)

X_std = np.std(x,axis=0)
print('X cur std:',X_std)
Y_std = np.std(Y)
print('Y cur std:',Y_std)

Piy = []
for i in range(len(X_std)):
    Piy.append(regr.coef_[i]*(X_std[i]/Y_std))
print(Piy)
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
