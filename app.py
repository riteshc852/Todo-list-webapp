from flask import Flask, render_template , request , redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# ------------------- MODEL -------------------
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False , default= "no content")
    desc = db.Column(db.String(200), nullable=False)
    title = db.Column(db.String(200) , nullable = False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return f"{self.sno} - {self.title}"

# ------------------- ROUTE -------------------
@app.route("/" ,methods=["GET" , "POST"])
def index():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title = title, desc = desc)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()  # print(allTodo) # for debugging
    return render_template('index.html' , allTodo = allTodo)  # Render HTML template
@app.route("/update/<int:sno>" , methods=["GET", "POST"])
def update(sno): 
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno = sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template("update.html", todo=todo)
@app.route("/delete/<int:sno>")
def delete(sno): 
    todo = Todo.query.filter_by(sno = sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")
# ------------------- MAIN -------------------
if __name__ == "__main__":
    # Create database tables inside application context
    with app.app_context(): # this is to create the database file 
        db.create_all()
    app.run(debug=False)
