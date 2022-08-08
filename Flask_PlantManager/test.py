import psycopg2 as pg2

conn = pg2.connect(database='PlantManager', user='postgres', password='secretpassword123')
cur = conn.cursor()
cur.execute("SELECT username FROM employees WHERE id = 1")
username = cur.fetchone()[0]

print(username)