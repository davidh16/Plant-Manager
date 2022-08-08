import string
import random
import psycopg2 as pg2

file = open('password.txt')
db_password = file.read()

def generate_password():
    #ova funkcija generira nasumičnu lozinku za novo registriranog zaposlenika

    characters = list(string.ascii_letters + string.digits + "!@#$%")
    lenght = 8
    random.shuffle(characters)
    password = []
    for i in range(lenght):
        password.append(random.choice(characters))
    random.shuffle(password)
    generated_password = "".join(password)
    return generated_password

def create_nickname(ime,prezime):
    #ova funkcija kreira korisničko ime na temelju dobivenog imena i prezimena, u slučaju da već postoji isto korisničko ime, funckija dodaje broj počevši od broja 1

    created_nickname = ime.lower() + prezime.lower()[0]
    conn = pg2.connect(database='PlantManager', user='postgres', password=db_password)
    cur = conn.cursor()
    cur.execute('SELECT * FROM employees WHERE username=%s', (created_nickname,))
    data = cur.fetchone()
    i=1
    if data:
        created_nickname += str(i)
        cur.execute('SELECT * FROM employees WHERE username=%s', (created_nickname,))
        data = cur.fetchone()
    while data :
        created_nickname = created_nickname.replace(str(i),str(i+1))
        i += 1
        cur.execute('SELECT * FROM employees WHERE username=%s', (created_nickname,))
        data = cur.fetchone()
    return created_nickname

def user_identification(username):
    #ova funkcija utvrđuje razinu pristupa određenog korisnika
    #razinu pristupa vraća kako bi se kasnije na temelju iste rendero screen za pojedini access level

    conn = pg2.connect(database='PlantManager', user='postgres', password=db_password)
    cur = conn.cursor()
    cur.execute('SELECT access_level FROM employees WHERE username=%s', (username,))
    access_level = cur.fetchone()
    return access_level[0]