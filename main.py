# coding=utf-8
# 主程序

import pandas as pd
import arcpy
from arcpy import env
import pymysql
from os import path

cur = path.dirname(__file__)
base_gdb = path.join(cur, 'jiaoke.gdb')


def get_data_from_mysql(time, sql='', charset='utf8'):
    conn = pymysql.connect(host='localhost', user='user1', password='123456', db='jiaoke', charset=charset)
    df = pd.read_sql(sql, con=conn)
    df.to_csv(path.join(cur, 'sample/sample{}.csv'.format(time)), encoding='gbk')
    return path.join(cur, 'sample/sample{}.csv'.format(time))


def edges_to_feature(edges_path=r'F:\jtkjds\data2\wlmqGIS_from OSM\edges'):
    env.workspace = edges_path
    arcpy.FeatureClassToGeodatabase_conversion('edges.shp', base_gdb)


def gps_point_to_feature(gps_path, gps_name, lat='lat', lon='lon'):
    arcpy.MakeXYEventLayer_management(gps_path, lat, lon, gps_name, 'WGS 1984')
    arcpy.SaveToLayerFile_management(gps_name, path.join(cur, '{}.lyr'.format(gps_name)))
    arcpy.FeatureClassToGeodatabase_conversion(path.join(cur, '{}.lyr'.format(gps_name)),
                                               base_gdb)


def create_buffer():
    env.workspace = base_gdb

    # 做缓冲区
    # print 'Buffer'
    buffer = arcpy.Buffer_analysis('edges', '#', '20 Meters', 'FULL', 'ROUND', 'ALL', '#', 'PLANAR')
    buffer_path = buffer.getOutput(0)  # buffer的路径
    buffer_name = buffer_path.split('\\')[-1]
    return buffer_name


def create_intersect(gps_name, buffer_name):
    env.workspace = base_gdb
    GPS_Intersect = arcpy.Intersect_analysis([base_gdb+'\{}'.format(gps_name), buffer_name], '#', 'ALL', '#', 'INPUT')
    GPS_Intersect_path = GPS_Intersect.getOutput(0)  # 相交后GPS数据的路径
    GPS_Intersect_Name = GPS_Intersect_path.split('\\')[-1]
    return GPS_Intersect_Name


def near_analysis(GPS_Intersect_Name, Road_Name='edges'):
    # GPS数据，对Road路网，做近邻分析
    env.workspace = base_gdb
    arcpy.Near_analysis(GPS_Intersect_Name, Road_Name, '#', 'LOCATION', 'NO_ANGLE', 'PLANAR')


def update_gps_point(gps_name):
    dic = {}
    cursor = arcpy.da.SearchCursor(path.join(base_gdb, gps_name), ['OBJECTID', 'NEAR_X', 'NEAR_Y'])
    for row in cursor:
        dic[row[0]] = [row[1], row[2]]
    del cursor
    del row

    # 更新几何
    cursor = arcpy.da.UpdateCursor(path.join(base_gdb, gps_name), ['OBJECTID', 'SHAPE@XY'])
    for row in cursor:
        row[1] = dic[row[0]]
        cursor.updateRow(row)
    del cursor
    del row


def calculate_v_and_num(GPS_Insert_Name, speed_name='speed'):
    cursor = arcpy.da.SearchCursor(path.join(base_gdb, GPS_Insert_Name),
                                   ['NEAR_FID', speed_name])
    dic = {}
    for row in cursor:
        if row[0] in dic.keys():
            dic[row[0]].append(row[1])
        else:
            dic[row[0]] = [row[1]]
    for id in range(1, 12107):
        if id not in dic.keys():
            dic[id] = [120, ]

            # for key in dic.keys():
            #     dic[key] = sum(dic[key]) / len(dic[key])
            # print dic[key]
    sorted(dic.keys())
    return dic


if __name__ == '__main__':
    edges_to_feature()
    buffer_name = create_buffer()

    all_edges_dic = {}

    for time in range(100000, 103000, 500):
        sql = 'select * from czc_gps WHERE acttime >={} AND acttime <{}'.format(time, time + 500)
        gps_path = get_data_from_mysql(time, sql, charset='gbk')
        gps_name = 'gps_{}'.format(time)
        gps_point_to_feature(gps_path, gps_name)
        GPS_Intersect_Name = create_intersect(gps_name, buffer_name)
        near_analysis(GPS_Intersect_Name)
        # update_gps_point(gps_name)
        dic = calculate_v_and_num(GPS_Intersect_Name, speed_name='speed')

        with open(path.join(cur, 'edges_info/{}.csv'.format(time)), 'w') as csv_file:
            csv_file.write(
                "OBJECTID,speed,num\n"
            )
            for key in dic.keys():
                csv_file.write(
                    ','.join([
                        str(key),
                        str(sum(dic[key]) / len(dic[key])),
                        str(len(dic[key]))
                    ]) + '\n'
                )
