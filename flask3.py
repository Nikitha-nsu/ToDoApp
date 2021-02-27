# -*- coding: utf-8 -*-
"""
Created on Sat Feb 27 15:39:01 2021

@author: Nikitha
"""


from flask import Flask
from flask_restful import Api,Resource,reqparse,abort,fields,marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///C:/Users/Nikitha/.spyder-py3/Flask API Tutorial/sqlite.db'
db = SQLAlchemy(app)

resource_fields = {
                    "id" : fields.Integer(),
                    "task" : fields.String(),
                    "summary" : fields.String()}

todo_post_args = reqparse.RequestParser()
todo_post_args.add_argument("task", type= str, help = "Task is required", required = True)
todo_post_args.add_argument("summary", type= str,help = "Summary is required", required = True)

todo_put_args = reqparse.RequestParser()
todo_put_args.add_argument("task", type= str)
todo_put_args.add_argument("summary", type= str)

class ToDoModel(db.Model):
        id = db.Column(db.Integer,primary_key=True)
        task = db.Column(db.String(200))
        summary = db.Column(db.String(200))
                
db.create_all()

class ToDoList(Resource):
    def get(self):
        tasks = ToDoModel.query.all()
        todos = {}
        for task in tasks:
            todos[task.id] = {"task": task.task, "summary": task.summary}  
        return todos
    
class ToDobyId(Resource):
       
    @marshal_with(resource_fields)
    def get(self,todo_id):
        task = ToDoModel.query.filter_by(id=todo_id).first()
        if not task:
            abort("Could not find Task id!")
        return task
    
    @marshal_with(resource_fields)    
    def post(self,todo_id):
        args = todo_post_args.parse_args()
        task = ToDoModel.query.filter_by(id=todo_id).first()
        if task:
            abort("Task already present!")
        todo = ToDoModel(id=todo_id, task = args["task"], summary = args["summary"])
        db.session.add(todo)
        db.session.commit()
        return todo,201
        
    @marshal_with(resource_fields)
    def put(self,todo_id):
        args=todo_put_args.parse_args()
        task=ToDoModel.query.filter_by(id = todo_id).first()
        if not task:
            abort("Task does not exist to update!")
        if args["task"]:
            task.task = args["task"]
        if args["summary"]:
            task.summary = args["summary"]
        db.session.commit()
        return task
        
    def delete(self,todo_id):
         task=ToDoModel.query.filter_by(id = todo_id).first()
         if not task:
             abort("Task not available to delete")
         db.session.delete(task)
         db.session.commit()
         return "Task Deleted", 204
        
api.add_resource(ToDoList, "/todos")
api.add_resource(ToDobyId, "/todos/<int:todo_id>")

if __name__ == "__main__":
    app.run(debug=True,use_reloader=False)