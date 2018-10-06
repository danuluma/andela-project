import psycopg2

conn = psycopg2.connect(user='postgres', host='localhost', password='postgres')
cur = conn.cursor()
cur.execute("""CREATE DATABASE mafast1;""")
cur.execute("""CREATE DATABASE tfast;""")
conn.commit()
conn.close()
cur.close()
print("Congrats!! Danns database created")
