import psycopg2 as pg2

file = open('password.txt')
db_password = file.read()

def item_existence(data):
    conn = pg2.connect(database='PlantManager', user='postgres', password=db_password)
    cur = conn.cursor()
    cur.execute('SELECT * FROM skladište WHERE naziv=%s AND proizvođač=%s AND dobavljač=%s AND tip=%s AND model=%s AND kataloški_broj=%s',
                (data['name'],data['brand'],data['supplier'],data['type'],data['model'],data['catalogue_number']))
    existance = cur.fetchone()
    if existance:
        return True
    return False