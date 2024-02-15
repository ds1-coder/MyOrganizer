from flask import (
    Flask,
    flash, 
    render_template, 
    redirect,
    request,
    url_for,
)
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#import os
#def printLog(*args, **kwargs):
#    print(*args, **kwargs)
#    with open('o.out','a') as file:
#        print(*args, **kwargs, file=file)
#printLog('hello Jos 1')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)

class Todo(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  content = db.Column(db.String(200), nullable = False)
  date_created = db.Column(db.DateTime, default = datetime.utcnow)
  
  def __repr__ (self):
    return '<Task %r>' % self.id

app.app_context().push()
@app.route("/", methods = ['POST', 'GET'])
def index():
  if request.method == "POST":
    #return "Hello!"
    task_content = request.form["content"]
    new_task = Todo(content=task_content)
    
    try:
      db.session.add(new_task)
      db.session.commit()
      return redirect('/')
    except:
      return "There was an issue adding your task"
      
  else:
    tasks = Todo.query.order_by(Todo.date_created).all()
    return render_template("index.html", tasks=tasks) 
  #return redirect(url_for('index'))

  
@app.route("/delete/<int:id>", methods = ["GET", "POST"])
def delete(id):
  task_to_delete = Todo.query.get_or_404(id)
  #printLog("task to delete: ", task_to_delete)
  try:
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect('/')
  except:
    return "There is a problem with deleting that task"

  
@app.route("/update/<int:id>", methods = ["GET", "POST"])
def update(id):
  task_to_update = Todo.query.get_or_404(id)

  if request.method == "POST":
      task_to_update.content = request.form['content'] 
      try:
        db.session.commit()
        return redirect('/')
      except:
        return "There is an issue with commiting the updated task"
    #tasks = Todo.query.order_by(Todo.date_created).all()
    #try:
     # return render_template("index.html", tasks=tasks)  
  else:
    return render_template("update.html", task=task_to_update)
    
    
if __name__ == '__main__':
  app.run(debug=True)