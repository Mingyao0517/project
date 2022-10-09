# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 20:32:35 2019

@author: zmy
"""
import numpy as np
import math
import collections
from sklearn import preprocessing,datasets,linear_model
import pandas as pd

#x = np.array([[24.7849,13.5036,15.6111,31.2494],           #数据格式因该是 横向 x1 x2 ，，，，
#              [56.6593,86.7704,93.3127,69.8421],
#              [55.8005,88.6280,68.9021,113.7907],
#              [65.0791,88.3041,91.5868,80.6926],
#              [125.9283,135.0274,140.6267,139.9881],
#              [112.5840,126.0310,112.6886,157.5936],
#              [41.4236,36.8813,26.0484,56.7237],
#              [32.9571,37.6037,26.9444,50.7283]])
#
#y = np.array([21.2872,73.1462,81.7803,81.4157,135.3701,127.2243,40.2691,37.3084])


data = pd.read_csv('data/data.csv')
np_data = data.values
print(np_data)
y = np_data[:,-1]
x = np_data[:,0:-1]


print('method1:指定均值方差数据标准化(默认均值0 方差 1):')
print('使用scale()函数 按列标准化')
x_scaled = preprocessing.scale(x,axis=0)
print('x 标准化后矩阵为:\n',x_scaled)
y_scaled = preprocessing.scale(y)
print(('y 标准化后矩阵为:',y_scaled))
X = x_scaled[:,:]
Y = y_scaled[:]
print(X,Y)

# 训练数据
regr = linear_model.LinearRegression()
regr.fit(X,Y)

print('(b1,b2...):',regr.coef_)
print('(b0):',regr.intercept_)

Py = list(regr.coef_)
print(Py)


def calcMean(x,y):
    sum_x = sum(x)
    sum_y = sum(y)
    n = len(x)
    x_mean = float(sum_x+0.0)/n
    y_mean = float(sum_y+0.0)/n
    return x_mean,y_mean
def pearson_demo(x,y):
    x_mean,y_mean = calcMean(x,y)	#计算x,y向量平均值
    n = len(x)
    sumTop = 0.0
    sumBottom = 0.0
    x_pow = 0.0
    y_pow = 0.0
    for i in range(n):
        sumTop += (x[i]-x_mean)*(y[i]-y_mean)
    for i in range(n):
        x_pow += math.pow(x[i]-x_mean,2)
    for i in range(n):
        y_pow += math.pow(y[i]-y_mean,2)
    sumBottom = math.sqrt(x_pow*y_pow)
    p = sumTop/sumBottom
    return p
Rij = {}
Rij = collections.OrderedDict()

RijB = {}
RijB =  collections.OrderedDict()
#




print('\n\n\n\n\n')

for i in range((x_scaled.shape)[1]-1):
    
    for j in range(i+1,(x_scaled.shape)[1]):
        print(x_scaled[:,i])
        print(x_scaled[:,j])
        res = pearson_demo(list(x_scaled[:,i]),list(x_scaled[:,j]))
#        RijB['R'+str(i+1)+str(j+1)+'B'+str(i+1)] = res * Py[i]
#        RijB['R'+str(i+1)+str(j+1)+'B'+str(j+1)] = res * Py[j]
        RijB['R'+str(i+1)+str(j+1)] = res * Py[j]
        RijB['R'+str(j+1)+str(i+1)] = res * Py[i]
        Rij['R'+str(i+1)+str(j+1)] = res
        Rij['R'+str(j+1)+str(i+1)] = res
        
sum_RB = {}#求间j
sum_RB = collections.OrderedDict()
for key in RijB.keys():
    if key[1] in sum_RB.keys():
        sum_RB[key[1]] = sum_RB[key[1]] + RijB[key]
    else:
        sum_RB[key[1]] =  RijB[key]

sum_force={}
sum_force = collections.OrderedDict()
for k in sum_RB.keys():
    sum_force[k] = sum_RB[k] +  Py[int(k)-1]
    
    
R = {} #决策系数
R = collections.OrderedDict()
for k in sum_force.keys():
    R[k] = 2 * Py[int(k)-1] * sum_force[k] - Py[int(k)-1] * Py[int(k)-1]
    
RijB = sorted(RijB.items(),key=lambda x:x[0])
sorted_RijB = {}
sorted_RijB = collections.OrderedDict()

for (p1,p2) in RijB:
    print(p1,p2)
    sorted_RijB[p1] = p2



n = x.shape[1] - 1
data_to_html = []
for i in range(len(list(sum_RB.keys()))):
    for j in range(n):
        #print(key,Rij[key])
        data_to_html.append({"tab1":"x"+str(i+1)+"对y    |",
                             "tab2":str(Py[i])+"   | ",
                             "tab3":str(list(sorted_RijB.keys())[i*n+j])+"-->"+"y    |",
                             "tab4":str(list(sorted_RijB.values())[i*n+j])+"    |",
                             "tab5":str(list(sum_RB.values())[i])+"    |",
                             "tab6":str(list(sum_force.values())[i])+"   | ",
                             "tab7":str(list(R.values())[i])+"    |"
                             
                            })
        
    
    

        
    
    
    
        
        
        





        

    
    
    
    
