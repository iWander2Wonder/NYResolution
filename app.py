from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)


# Create the application context globally
ctx = app.app_context()
ctx.push()  # Push the context


class Task(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   description = db.Column(db.String(255), nullable=False)
   completed = db.Column(db.Boolean, default=False)


db.create_all()


@app.route('/')
def index():
   tasks = Task.query.order_by(Task.completed).all()
   return render_template('index.html', tasks=tasks)


@app.route('/add_task', methods=['POST'])
def add_task():
   description = request.form['description']
   task = Task(description=description)
   db.session.add(task)
   db.session.commit()
   return redirect(url_for('index'))


@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
   task = Task.query.get_or_404(task_id)
   if request.method == 'POST':
       task.description = request.form['description']
       task.completed = request.form.get('completed') == 'on'
       db.session.commit()
       return redirect(url_for('index'))
   return render_template('edit_task.html', task=task)


@app.route('/toggle_task/<int:task_id>')
def toggle_task(task_id):
   task = Task.query.get_or_404(task_id)
   task.completed = not task.completed
   db.session.commit()
   return redirect(url_for('index'))


@app.route('/delete_task/<int:task_id>')
def delete_task(task_id):
   task = Task.query.get_or_404(task_id)
   db.session.delete(task)
   db.session.commit()
   return redirect(url_for('index'))


if __name__ == '__main__':
   with app.app_context():  # Ensure context is active within the main block
       app.run(debug=True)