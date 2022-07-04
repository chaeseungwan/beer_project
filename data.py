import psycopg2 as pg2
import pandas.io.sql as psql


conn = pg2.connect(
    host = 'arjuna.db.elephantsql.com',
    database = 'smskhciq',
    user="smskhciq",
    password="eKJl8MkMUHacWAL8_d_1BJUfF_uHk21m",
    )

# 인스턴스 생성
cur = conn.cursor()

def data_load(sql_queery):
    return psql.read_sql(sql_queery, conn)
