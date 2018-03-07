# coding=utf8
import arcpy
import pandas as pd

df1 = pd.read_csv('C:\\Users\\D\\Desktop\\base.csv')
df2 = pd.read_csv('C:\\Users\\D\\Desktop\\zhanshi.csv')
dic = {}
for i in range(1, len(df1.keys()) - 1, 2):
    if len(df2.keys()[i]) == 3:
        dic[df1.keys()[i]] = ''.join(['201710120', df2.keys()[i], '00'])
    else:
        dic[df1.keys()[i]] = ''.join(['20171012', df2.keys()[i], '00'])

cursor = arcpy.da.UpdateCursor("F:/arcgiscode/jiaoke.gdb/edges_TransposeFields", ['time'])
for row in cursor:
    row[0] = dic[row[0]]
    cursor.updateRow(row)
