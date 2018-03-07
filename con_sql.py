import pymysql
import pandas
conn = pymysql.connect(host='localhost', user='user1', password='123456', db='jiaoke', charset='gbk')
# sql = 'select * from czc_gps where acttime>=90000 and acttime<=90500'
# df = pd.read_sql(sql, con=conn)
# print df[:10]
conn.close()
