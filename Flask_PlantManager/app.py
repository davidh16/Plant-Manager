from flask import Flask, make_response, request, session
from flask_restful import Api
import datetime
import psycopg2 as pg2
import jwt
from api.admin_routes import admin_blueprint
from api.warehouse_manager_routes import warehouse_manager_blueprint
from api.worker_routes import worker_blueprint
from api.shift_manager_routes import shift_manager_blueprint

app = Flask(__name__)
api = Api(app)
app.register_blueprint(admin_blueprint)
app.register_blueprint(warehouse_manager_blueprint)
app.register_blueprint(worker_blueprint)
app.register_blueprint(shift_manager_blueprint)

SECRET_KEY = 'secretkey123'

file = open('password.txt')
db_password = file.read()

@app.route('/login', methods=['POST'])
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response({'message': 'Could not verify'})

    conn = pg2.connect(database='PlantManager', user='postgres', password=db_password)
    cur = conn.cursor()
    cur.execute("SELECT * FROM employees WHERE username = %s", (auth.username,))
    user = cur.fetchone()

    if user:
        if user[13] == auth.password:
            token = jwt.encode({'access_level': user[5], 'user_id' : user[0], 'exp' : datetime.datetime.utcnow() + datetime.timedelta(hours=8)}, SECRET_KEY,algorithm='HS256')
            cur.execute("UPDATE employees SET last_login = NOW() WHERE username = %s", (auth.username,))
            conn.commit()
            return {'token': token}

    return make_response({'message': 'Wrong username or password, please try again or contact your administrator'})

@app.route('/logout', methods=['GET'])
def logout():

    conn = pg2.connect(database='PlantManager', user='postgres', password=db_password)
    cur = conn.cursor()
    cur.execute("UPDATE employees SET last_logout = NOW() WHERE id = %s", (session['user'],))
    conn.commit()
    return make_response({'message': 'User logged out'})


if __name__ == "__main__":
    app.run(port = 8000, debug = True)