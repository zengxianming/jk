import arcpy

cursor = arcpy.da.SearchCursor("C:\\Users\\D\\Documents\\ArcGIS\\Default.gdb\\gj_shot_Intersect", ['NEAR_FID', 'gpsspeed'])
dic = {}
for row in cursor:
    if row[0] in dic.keys():
        dic[row[0]].append(row[1])
    else:
        dic[row[0]] = [row[1]]

for key in dic.keys():
    dic[key] = sum(dic[key]) / len(dic[key])
    # print dic[key]
del cursor
del row

cursor = arcpy.da.UpdateCursor("C:\\Users\\D\\Documents\\ArcGIS\\Default.gdb\\edges", ['OBJECTID', 'avg_speed'])
for row in cursor:
    if row[0] in dic.keys():
        row[1] = dic[row[0]]
    else:
        row[1] = 100
    cursor.updateRow(row)
del cursor
del row
