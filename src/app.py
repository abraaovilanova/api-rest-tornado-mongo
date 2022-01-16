import tornado.ioloop
import tornado.web

import json
import database
from bson import json_util
from bson.objectid import ObjectId

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world!")

class EmployeeHandler(tornado.web.RequestHandler):
    def post(self):
        new_employee = json.loads(self.request.body)

        db = database.db_connect()

        x = db.insert_one(new_employee)

        self.write({"Response":"New employee created!"})
    
    def get(self):
        db = database.db_connect()

        list_employees = [doc for doc in db.find({})]

        self.write({"Response": json.loads(json_util.dumps(list_employees))})

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