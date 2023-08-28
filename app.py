from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap5
from datetime import date
import os

db = SQLAlchemy()
app = Flask(__name__)
app.secret_key = os.urandom(20)

bootstrap = Bootstrap5(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
db.init_app(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=True, default=date.today(), )
    done = db.Column(db.Boolean, nullable=True, default=False)


with app.app_context():
    db.create_all()


class ToDoForm(FlaskForm):
    task = StringField('Task', validators=[DataRequired()])
    date = DateField('Date')
    submit = SubmitField("Add Task")


class EditForm(FlaskForm):
    task = StringField('Task', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()], format='%Y-%m-%d')
    submit = SubmitField("Edit")


@app.route('/', methods=["GET", "POST"])
def task_manager():
    form = ToDoForm()
    task_list = db.session.execute(db.select(Task).order_by(Task.task)).scalars().all()
    if form.validate_on_submit():
        task = Task(
            task=form.task.data,
            date=form.date.data,
        )
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('task_manager'))
    return render_template("index.html", form=form, task_list=task_list)


@app.route('/delete-task/<int:task_index>', methods=["GET", "POST"])
def delete_task(task_index):
    delTask = Task.query.get(task_index)
    db.session.delete(delTask)
    db.session.commit()
    return redirect(url_for('task_manager'))


@app.route('/edit-task/<int:task_index>', methods=["GET", "POST"])
def edit_task(task_index):
    task = Task.query.get(task_index)
    formated_date = task.date.split("-")
    form = EditForm(task=task.task, date=date(int(formated_date[0]), int(formated_date[1]), int(formated_date[2])))
    if form.validate_on_submit():
        task.task = form.task.data
        task.date = form.date.data
        db.session.commit()
        return redirect(url_for('task_manager'))
    return render_template("edit.html", form=form)


@app.route("/checked/<int:task_index>", methods=["GET", "POST"])
def check_task(task_index):
    task = Task.query.get(task_index)
    if not task.done:
        task.done = True
        db.session.commit()
        return redirect(url_for('task_manager'))
    else:
        task.done = False
        db.session.commit()
        return redirect(url_for('task_manager'))

if __name__ == '__main__':
    app.run(debug=True)
