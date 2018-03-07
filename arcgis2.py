# coding=utf8
# 更新edges字段及数据

import arcpy
import pandas as pd
from os import path

# 增加时间字段
# cur = path.dirname(__file__)
# df = pd.read_csv('C:\\Users\\D\\Desktop\\base.csv')
# columns = df.keys()
# for i in range(2, len(columns)-1, 2):
#     time = columns[i]
#     print time
#     arcpy.AddField_management("F:/arcgiscode/jiaoke.gdb/edges", time, 'float')
#     cursor = arcpy.da.UpdateCursor("F:/arcgiscode/jiaoke.gdb/edges", [time])
#     for j, row in enumerate(cursor):
#         row[0] = df[time][j]
#         cursor.updateRow(row)
#     del cursor

# 增加等级字段
# cur = path.dirname(__file__)
# df = pd.read_csv('C:\\Users\\D\\Desktop\\outbase.csv')
# arcpy.AddField_management("F:/arcgiscode/jiaoke.gdb/edges", 'level', 'text')
# cursor = arcpy.da.UpdateCursor("F:/arcgiscode/jiaoke.gdb/edges", ['level'])
# for i, row in enumerate(cursor):
#     row[0] = df['level'][i]
#     cursor.updateRow(row)

# 增加评分字段
cur = path.dirname(__file__)
arcpy.AddField_management("F:/arcgiscode/jiaoke.gdb/edges_TransposeFields", 'label', 'text')
cursor = arcpy.da.SearchCursor("F:/arcgiscode/jiaoke.gdb/edges_TransposeFields", ['level', 'speed'])
dic = {}
for i, row in enumerate(cursor):
    if row[0] == '1':
        f = lambda x: 1 if x > 65 else 2 if x > 50 else 3 if x > 35 else 4 if x > 20 else 5
        dic[i] = str(f(float(row[1])))
    elif row[0] == '2':
        f = lambda x: 1 if x > 40 else 2 if x > 30 else 3 if x > 20 else 4 if x > 15 else 5
        dic[i] = str(f(float(row[1])))
    elif row[0] == '3':
        f = lambda x: 1 if x > 35 else 2 if x > 25 else 3 if x > 15 else 4 if x > 10 else 5
        dic[i] = str(f(float(row[1])))

del cursor
del row
cursor = arcpy.da.UpdateCursor("F:/arcgiscode/jiaoke.gdb/edges_TransposeFields", ['label'])
for j, row in enumerate(cursor):
    row[0] = dic[j]
    cursor.updateRow(row)
del cursor
del row