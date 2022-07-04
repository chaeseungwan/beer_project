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


# cur.execute("CREATE TABLE IF NOT EXISTS beer_data(Name text, Style text, Brewery text, BeerName text, Description text, ABV float, \
#             MINIBU integer, MaxIBU integer, Astringency integer, Body integer, Alcohol integer, Bitter integer, Sweet integer, Sour integer, Salty integer, \
#             Fruits integer, Hoppy integer, Spices integer, Malty integer, review_aroma float, review_appearance float, review_palate  float, \
#             review_taste float,  review_overall float, number_of_reviews integer)")


# with open('data/commadel_rating.csv', 'r') as f:
#     next(f) # Skip the header row.
#     #f , <database name>, Comma-Seperated
#     cur.copy_from(f, 'beer_data', sep=',')
#     #Commit Changes
#     conn.commit()
#     #Close connection
#     conn.close()

# f.close()


sql_queery = 'SELECT * FROM beer_data'
df = psql.read_sql(sql_queery, conn)

print(df.columns)


