from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisisasecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    psw = db.Column(db.String(500), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<users {self.id}>"

class Profiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    old = db.Column(db.Integer)
    city = db.Column(db.String(100))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"<profiles {self.id}>"

@app.route('/')
def index():
    print( url_for('index'))
    return render_template("index.html", title="Главная")

@app.route('/register', methods=("POST", "GET"))
# @login_required
def register():
    if request.method == "POST":
        try:
            hash = generate_password_hash(request.form['psw'])
            u = User(email=request.form['email'], psw=hash)
            db.session.add(u)
            db.session.flush()
            p = Profiles(name=request.form['name'], old=request.form['old'],
            city=request.form['city'], user_id = u.id)
            db.session.add(p)
            db.session.commit()
        except:
            db.session.rollback()
            print("Ошибка добавления в БД")

    return render_template("register.html", title="Регистрация")

if __name__ == '__main__':
    app.run(debug=True) 