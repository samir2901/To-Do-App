from flask import Flask, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired
from datetime import datetime

class ToDoForm(FlaskForm):
    todo = TextAreaField("Enter todo", render_kw={"rows":35, "cols":20}, validators=[DataRequired()])
    submit = SubmitField("Submit")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SECRET_KEY'] = "my super secret key"

db = SQLAlchemy(app)

class ToDoData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(200), nullable=False, default="Not Complete") #Complete / Not Complete
    date_added = db.Column(db.DateTime, default=datetime.utcnow)    

    def __repr__(self) -> str:
        return '<ToDo %r>' % self.todo

@app.route("/", methods = ["GET","POST"])
def index():    
    form = ToDoForm()
    if form.validate_on_submit():
        data = ToDoData(todo=form.todo.data)
        db.session.add(data)
        db.session.commit()
        form.todo.data = ""
        flash("Todo Added Successfully!")
    todos = ToDoData.query.order_by(ToDoData.date_added)
    return render_template("index.html",form=form,todos=todos)

@app.route("/update/<int:id>")
def update(id):
    todo_to_update = ToDoData.query.get_or_404(id)    
    if todo_to_update.status == "Not Complete":
        todo_to_update.status = "Complete"
    else:
        todo_to_update.status = "Not Complete"
    try:        
        db.session.commit()        
    except:
        flash("There's an error!")
    return redirect(url_for('index'))
    

@app.route("/delete/<int:id>")
def delete(id):
    todo_to_delete = ToDoData.query.get_or_404(id)    
    try:
        db.session.delete(todo_to_delete)
        db.session.commit()
        flash("Task deleted successfully!!")
    except:
        flash("Error!")
    return redirect(url_for('index'))
    
