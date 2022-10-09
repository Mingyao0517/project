# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 09:40:06 2019

@author: zmy
"""

from flask import Flask,render_template, request, send_from_directory,jsonify
#import pandas as pd
#import numpy as np
import numpy as np
import math
import collections
from sklearn import preprocessing,datasets,linear_model
import pandas as pd

import os
import sys

base_path = os.path.dirname(os.path.realpath(__file__))  # 获取脚本路径
 
upload_path = os.path.join(base_path, 'upload')   # 上传文件目录
if not os.path.exists(upload_path):
    os.makedirs(upload_path)

app=Flask(__name__) #创建1个Flask实例
upload_file_folder = os.path.join(os.getcwd(),'upload')
#@app.route('/upload', method='GET')

def getData(path):
    data = pd.read_csv(path)
    np_data = data.values
    #print(np_data)
    y = np_data[:,-1]
    x = np_data[:,0:-1]
    
    
#    print('method1:指定均值方差数据标准化(默认均值0 方差 1):')
#    print('使用scale()函数 按列标准化')
    x_scaled = preprocessing.scale(x,axis=0)
    #print('x 标准化后矩阵为:\n',x_scaled)
    y_scaled = preprocessing.scale(y)
    #print(('y 标准化后矩阵为:',y_scaled))
    X = x_scaled[:,:]
    Y = y_scaled[:]
    #print(X,Y)
    
    # 训练数据
    regr = linear_model.LinearRegression()
    regr.fit(X,Y)
    
#    print('(b1,b2...):',regr.coef_)
#    print('(b0):',regr.intercept_)
    
    Py = list(regr.coef_)
    #print(Py)
    
    
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
#            print(x_scaled[:,i])
#            print(x_scaled[:,j])
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
        #print(p1,p2)
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
    return data_to_html
            
@app.route('/')      #路由系统生成 视图对应url,1. decorator=app.route() 2. decorator(first_flask)
def first_flask():    #视图函数
   
    
    
    
    data_to_html = getData('data/data.csv')
    
    return render_template("home.html", name="决策表", data=data_to_html)

def check_file_type(filename):
    file_type = [ 'jpg', 'doc', 'docx', 'txt', 'pdf', 'PDF','png', 'PNG', 'xls', 'rar', 'exe', 'md', 'zip','csv']
    # 获取文件后缀
    ext = filename.split('.')[1]
    # 判断文件是否是允许上传得类型
    if ext in file_type:
        return True
    else:
        return False


@app.route('/upload', methods=['POST','GET'])
def upload():
    import re
    file = request.files['fileField']#request.files.get('fileField')
    #filename = file.get('fileField')
    #print(str(file))
    if not file:
        return "请选择上传文件！"
    filename = re.findall(r'\'.*?.csv\'',str(file))#name = file>onchange="document.getElementById('textfield').value=this.value" 
    #print(upload_path+'\\'+filename[0][1:-1])
    file.save(os.path.join(upload_file_folder, file.filename))
    data_to_html = getData(upload_path+'\\'+filename[0][1:-1])
    print(data_to_html)
    #file.save(upload_path+'\\'+filename[0][1:-1])

    

    # 检查文件类型
    if check_file_type(file.filename):
        # 一句代码完成保存文件操作
        file.save(os.path.join(upload_file_folder, file.filename))
        return render_template('home.html', status='OK',name="决策表", data=data_to_html)
    else:
        return 'NO'

if __name__ == '__main__':
    app.run()