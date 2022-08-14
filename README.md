# Plant-Manager

The porpouse of this project is to showcase knowledge about backend developments using python and Flask framework.

The app is used for tracking quantity of parts in warehouse, tracking maintenance of machines and assigning task for maintenance.

There are four access levels (admin, warehouse_manager, shift_manager and worker) and for each one of these there are actions that can be performed. 

Admin can register, update and delete users (employees).
Warehouse_manager can add and update items (parts) that warehouse contains.
Shift_manager can assign tasks to workers (maintenance) and see all tasks that are in progress.
Worker can view if certain parts are available in warehouse and complete tasks that are assigned by shift_manager.

Everything is connected to a database which is runned by postgresql.

There are few employees that have been already created.

username : admina
password : admin
access_level : admin

username : eliotg
password : password
access_level : warehouse_manager

username : johns
password : password
access_level : shif_manager

username : mackp
password : password
access_level : worker

Testing is done by Postman, there is Postman collection which can be imported.


