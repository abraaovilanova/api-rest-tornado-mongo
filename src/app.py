import tornado.ioloop
import tornado.web

import json
from bson import json_util
from bson.objectid import ObjectId

import database
import utils

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world!")

class EmployeeHandler(tornado.web.RequestHandler):
    def post(self):

        list_mandatory = ['name','birth_date','gender','email','cpf','start_date']

        new_employee = json.loads(self.request.body)

        list_dict_keys = list(new_employee.keys())

        if not(utils.mandatory_keys_check(list_mandatory, list_dict_keys)):
            self.set_status(400)
            self.write('Fail to create an Employee. Please check your data')
            return None

        db = database.db_connect()

        x = db.insert_one(new_employee)

        self.write("New employee created!")
    
    def get(self):
        db = database.db_connect()

        list_employees = [doc for doc in db.find({})]

        if(len(list_employees)>0):
            self.write({"Response": json.loads(json_util.dumps(list_employees))})
        else:
            self.write("Empty database")

class EmployeesHandler(tornado.web.RequestHandler):
    def get(self, _id):
        objInstance = ObjectId(_id)

        db = database.db_connect()

        x = db.find_one({"_id":objInstance})

        self.write({"res": json.loads(json_util.dumps(x))})
    
    def put(self, _id):
        newvalues = json.loads(self.request.body)

        objInstance = ObjectId(_id)

        db = database.db_connect()

        x = db.update_one({"_id": objInstance}, {"$set": newvalues})

        self.write({"res": "Employee updated"})
    
    def delete(self, _id):
        objInstance = ObjectId(_id)

        db = database.db_connect()

        x = db.delete_one({"_id": objInstance})

        self.write({"res":"Employee deleted"})

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/employee", EmployeeHandler),
        (r"/employee/([^/]+)?", EmployeesHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()