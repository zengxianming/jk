# coding:utf-8
# 地图匹配与GPS位置点更新
import arcpy
from arcpy import env
env.workspace = r'C:\\Users\\D\\Documents\\ArcGIS\\Default.gdb'

dic = {}
cursor = arcpy.da.SearchCursor("C:\\Users\\D\\Documents\\ArcGIS\\Default.gdb\\gj_shot_Intersect",
                               ['OBJECTID', 'NEAR_X', 'NEAR_Y'])
for row in cursor:
    dic[row[0]] = [row[1], row[2]]
del cursor
del row

# 更新几何
cursor = arcpy.da.UpdateCursor("C:\\Users\\D\\Documents\\ArcGIS\\Default.gdb\\gj_shot_Intersect", ['OBJECTID', 'SHAPE@XY'])
for row in cursor:
    row[1] = dic[row[0]]
    cursor.updateRow(row)
del cursor
del row
