# -*- coding: utf-8 -*-
import pymysql
import pandas as pd
from sqlalchemy import create_engine
import os


# 确定需连接的数据库
def database_connect(my_host,my_user,my_password,database_name):
    '''
    作用：
        连接数据库
    输入：
        my_host:IP地址
        my_user:用户名
        my_password:密码
        database_name:数据库名
    输出：
        conn:连接路径
    '''
    conn = pymysql.connect(host=my_host,user= my_user,password=my_password,database=database_name)
    return conn


# 设置数据库链接路径
#conn = database_connect("localhost","root","123456",'历史气象数据_风速')


# 有选择性的查询数据
def get_data(conn,features,table_name):
    '''
    作用：
        查询数据库中某表里的部分数据
    输入：
        conn:数据库路径
        features:希望查询的特征
        table_name:希望查询的表名
    输出：
        data_out:查询得到的数据，格式为pandas.dataframe
    '''
    conn.ping(reconnect=True)
    cursor = conn.cursor()
    data_out = pd.DataFrame()
    a = features[0]
    for i in range(len(features)-1):
        a = a + ','+ features[i+1]
    sql = "select "  + a + " from " + table_name
    cursor.execute(sql)
    data = cursor.fetchall()
    data_out = data_out.append(list(data))
    data_out = data_out.reset_index(drop=True)
    data_out.columns = features
    cursor.close()
    conn.close()
    return data_out
# get_data(conn,['X11','X12','X13'],"reg_kgl_00005_test")


# 查询表中全部数据
def get_data_all(conn,table_name):
    '''
    作用：
        查询数据库中某表里的全部数据
    输入：
        conn:数据库路径
        table_name:希望查询的表名
    输出：
        data_out:查询得到的数据，格式为pandas.dataframe
    '''
    conn.ping(reconnect=True)
    cursor = conn.cursor()
    data_out = pd.DataFrame()
    sql = "select * from " + table_name
    cursor.execute(sql)
    data = cursor.fetchall()
    data_out = data_out.append(list(data))
    cursor.close()
    conn.close()
    return data_out


# 创建新表
def create_table(conn,table_name,name):
    """
    作用：
        在mysql数据库中创建表格
    输入：
        conn:待创表格的数据库
        table_name:待创表格的表格名，eg.'表格名'
        name:待创表格的字段名，包含字段类型,eg.'Id int, salary float'
    """
    sql = "create table "+ table_name + "(" + name + ")"
    conn.ping(reconnect=True)
    cursor = conn.cursor()
    cursor.execute(sql)
    cursor.close()
    conn.close()
    return


# 存入所有所得数据
def insert_data_all(data,user,password,host,database,table_name):
    """
    作用：
         把全部数据存储进mysql数据库中
    输入：
        data:待存入的数据，为pandas.dataframe结构
        user:用户名
        password:密码
        host:地址
        database:数据库名
        table_name:待存入数据的表名
    """
    connect = create_engine("mysql+pymysql://"+user+":"+password+"@"+host+"/"+database)
    pd.io.sql.to_sql(data, table_name, connect, schema=database, if_exists="append",index=False)
    return
# insert_data_all(data,'intern','123456','10.75.4.20','ml_competition','reg_kgl_0005_test')


# 有筛选的存入数据
def insert_data(data,user,password,host,database,table_name,features):
    '''
    作用：
        把部分数据存储进mysql数据库中
    输入：
        data:待存入的数据，为pandas.dataframe结构
        user:用户名
        password:密码
        host:地址
        database:数据库名
        table_name:待存入数据的表名
        features:希望存入的特征列
    '''
    data_in = data[features]
    connect = create_engine("mysql+pymysql://"+user+":"+password+"@"+host+"/"+database)
    pd.io.sql.to_sql(data_in, table_name, connect, schema=database, if_exists="append",index=False)
    return
#insert_data(data,'intern','123456','10.75.4.20','ml_competition','reg_kgl_0005_test',['X5','X6','X8'])


#new_environ['‪B:/cisdi/ml_competition/round2/Taxi/test.csv'] = os.path.abspath(new_environ['‪B:/cisdi/ml_competition/round2/Taxi/test.csv'].encode('mbcs', 'replace'))
#data = pd.read_csv('B:\cisdi\ml_competition\round4\lq\train.csv')
#data = pd.read_csv('C:/Users/tianxinxin/Desktop/sjk/digraph.csv')
#cities = ['am','cz','dg','佛山','广东','广州','河源','惠州','江门','揭阳','茂名','梅州','清远','汕头','汕尾','韶关','深圳',
          #'阳江','云浮','湛江','肇庆','中山','珠海']
cities = ['am','cz','dg','fs','gd','广州','hy','hz','jm','jy','mm','mz','qy','st','sw','sg','sz',
          'yj','yf','zj','zq','zs','zh']
#feature = '温度'
#data = pd.read_excel(r'B:\CQU_JCI\国创2020\数据库\城市\城市\气象预报数据.xlsx')
conn = database_connect("localhost","root","123456",'负荷预测结果')
for i in range(23):
    city_name = cities[i]
    table_name = 'forecasting_' + city_name
    sql ='create table ' + table_name + '(city varchar(100),Date varchar(100) not null,Loads float)'
    cursor = conn.cursor()
    cursor.execute(sql)

    #data_city = data[(data['city']==city_name) & (data['weather']==feature)]
    #data_city = data_city.drop(columns=['weather','createtime', 'updatetime'])
    #insert_data_all(data_city, 'root', '123456', 'localhost', '历史气象数据_温度',table_name)
