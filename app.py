from flask import Flask, render_template, url_for, redirect, request
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap5
import os

app = Flask(__name__)
app.secret_key = os.urandom(20)
bootstrap = Bootstrap5(app)


class ToDoForm(FlaskForm):
    task = StringField('Task', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    submit = SubmitField("Add Task")


task_list = []


@app.route('/', methods=["GET", "POST"])
def task_manager():
    form = ToDoForm()
    if form.validate_on_submit():
        task_list.append((form.task.data, form.date.data))
        return redirect(url_for('task_manager'))
    return render_template("index.html", form=form, task_list=task_list)


@app.route('/task-delete/<int:task_index>', methods=["GET", "POST"])
def delete_task(task_index):
    del task_list[task_index]
    return redirect(url_for('task_manager'))


if __name__ == '__main__':
    app.run(debug=True)
