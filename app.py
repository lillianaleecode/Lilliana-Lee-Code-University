from flask import Flask, render_template, url_for, request, redirect #when it says name error is not defined, I need to add it here
from flask_sqlalchemy import SQLAlchemy
# pip install flask-sqlalchemy
from datetime import datetime

app = Flask (__name__ )
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///test.db'
#initialize the database
db = SQLAlchemy(app) 

#create a database model
class Todolist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200),nullable=False)
    completed = db.Column(db. Integer, default=0)
    data_created = db.Column(db.DateTime, default=datetime.utcnow)

    #create a function to return a string when  we add
    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']#if we submit our form, it will give this value, content is from the content form in our index
        new_task = Todolist(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect ('/')
        except:
            return 'there is an issue adding your request'
    else:
        tasks = Todolist.query.order_by(Todolist.data_created).all() #here I created the variable 'tasks'
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todolist.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
        
    except:
        return 'there was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    task = Todolist.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect ('/')

        except: 
            return 'there was an issue updating your task'

    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    app.run(debug=True)