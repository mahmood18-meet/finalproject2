from flask import Flask, flash,redirect, render_template, request, session, abort
import os
from flask_sqlalchemy import SQLAlchemy
# from flask.ext.session import Session

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://hxbltojwmjnbff:1f93289a19911ffc3152420fef4e14b16421f786811ad48d3aedca88958256c3@ec2-50-16-231-2.compute-1.amazonaws.com:5432/d6tghj3nmll0iu'
db = SQLAlchemy(app)
# sess = Session()

class User(db.Model) :
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    email = db.Column(db.String(30), unique = True, nullable = False)
    password = db.Column(db.String(30), nullable = False)
    #name = db.Column(db.String(30), nullable = False)

    #def __repr__(self) :
       # return '<User %r>' % self.username


@app.route('/')
def home():
    return render_template("home.html")
@app.route('/calendar', methods = ['GET' , 'POST'])
def calendar():
    return render_template("calendar.html")
@app.route('/tips' , methods = ['GET' , 'POST'])
def tips():
    return render_template("tips.html")
@app.route('/thingstodo' , methods = ['GET' , 'POST'])
def thingstodo():
    return render_template("thingstodo.html" , methods = ['GET' , 'POST'])


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    # Check if there is a used email such as this.
    if request.method == 'POST':
        email = request.form.get('Gmail')
        users_with_email = User.query.filter_by(email = email).all()
        if len(users_with_email) == 0:
            new_user = User()
            new_user.email = request.form['email']
            new_user.password = request.form['psw']
            db.session.add(new_user)
            db.session.commit()
            print(User.query.all())
            return redirect('calendar')
        else:
            return redirect('home')
    else:
        return redirect('home')


@app.route('/signin', methods = ['GET' , 'POST'])
def signin():
    if request.method == 'GET':
        return render_template('home.html')

    elif request.method == 'POST':
        user = User.query.filter_by(email=request.form['Gmail']).first()
        print(user)
        if user.password == request.form.get('psw'):
            session['signed_in'] = True
            return render_template('calendar.html', user= user)

        else:
            flask('Wrong Password!')
            return render_template('home.html')

if __name__ == '__main__':
   app.secret_key= 'super secret key'
   app.config['SESSION_TYPE'] = 'filesystem'
   # sess.init_app(app)
   app.run(debug = True)


