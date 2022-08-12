from flask import Flask, make_response, request
from flask_restful import Api
from flask_login import login_user, current_user, logout_user, login_required
from api.admin_routes import admin_blueprint
from api.warehouse_manager_routes import warehouse_manager_blueprint
from api.worker_routes import worker_blueprint
from api.shift_manager_routes import shift_manager_blueprint
from database import db, login_manager
from model.employees_model import Employee
from model.machines_model import Machine
import datetime

app = Flask(__name__)
api = Api(app)

app.config['SECRET_KEY']='secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres+psycopg2://postgres:secretpassword123@localhost:5432/PlantManager'
db.init_app(app)

app.register_blueprint(admin_blueprint)
app.register_blueprint(warehouse_manager_blueprint)
app.register_blueprint(worker_blueprint)
app.register_blueprint(shift_manager_blueprint)

login_manager.init_app(app)

@app.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return make_response({'message':'You are already logged in'})
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response({'message': 'Could not verify'})
    user = Employee.query.filter_by(username=auth.username).first()
    if user:
        if user.password == auth.password:
            user.last_login=datetime.datetime.utcnow()
            db.session.commit()
            login_user(user)
            return make_response({'message':'Logged in'})
    return make_response({'message': 'Wrong username or password, please try again or contact your administrator'})

@app.route('/logout', methods=['GET'])
def logout():
    if current_user.is_authenticated:
        user = Employee.query.filter_by(username=current_user.username).first()
        user.last_logout = datetime.datetime.utcnow()
        db.session.commit()
        logout_user()
        return make_response({'message': 'User logged out'})
    return make_response({'message':'You are not logged in'})

@app.route('/password_change', methods=['PUT'])
@login_required
def change_password():
    data = request.get_json()
    user = Employee.query.filter_by(username=current_user.username).first()
    if user.password == data['current_password'] and data['new_password'] == data['new_password2']:
        user.password = data['new_password']
        db.session.commit()
        return make_response({'message':'You have successfully changed your password'})
    return make_response({'message':'Could not change the password'})

with app.app_context():
    # db.create_all()
    # db.session.commit()
    machines_for_maintenance = Machine.query.all()
    for machine in machines_for_maintenance:
        if machine.last_maintenance + datetime.timedelta(days=machine.maintenance_freq) < datetime.datetime.utcnow():
            machine.maintenance_needed = True
            db.session.commit()
            db.session.close()

if __name__ == "__main__":
    app.run(port = 8000, debug = True)
