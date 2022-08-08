class Task:
    def __init__(self,machine, date_of_assignment,date_of_completion,status,description,description_of_work,machine_id):
        self.machine = machine
        self.date_of_assignment = date_of_assignment
        self.date_of_completon = date_of_completion
        self.status = status
        self.description = description
        self.description_of_work = description_of_work
        self.machine_id = machine_id