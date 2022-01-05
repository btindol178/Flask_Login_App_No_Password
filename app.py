from flask import Flask,render_template,flash,redirect,url_for
from flask_login import login_user
from datetime import datetime
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '5f4d94e1da3bd8871282c8e4b2586a87'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'


db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"

@app.before_first_request
def create_tables():
    db.create_all() 

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(20), nullable=False)


class UserForm(FlaskForm):
    user = StringField('Please enter your first name:', validators=[DataRequired()])
    submit = SubmitField('Register')


@app.route("/login",methods=['GET','POST'])
def Login():
    form = UserForm()
    if form.validate_on_submit():
        user1 = form.user.data
        print(user1)
        exists = User.query.filter_by(user=user1).first()
        print(exists.user)
        if exists is not None:
            flash(f'{exists.user} Congrats your logged in !', 'success')
            login_user(exists, remember=exists)
            return render_template("login.html",form=form)
        else:
            flash('User does not exist created!', 'success')
            return redirect(url_for('Sign_up'))
    return render_template("login.html",form=form)

@app.route("/logout")
def Logout():
    return "<h1> fart </h1>"

@app.route("/",methods=['GET','POST'])
@app.route("/new_user",methods=['GET','POST'])
def Sign_up():
    form = UserForm()
    if form.validate_on_submit():
        user1=form.user.data
        exists = User.query.filter_by(user=user1).first()
        if exists:
            flash(f'{exists.user} Exists login here at login page!')
            return redirect(url_for('Login'))
        else:
            new_user = User(user=form.user.data)
            print(new_user)
            db.session.add(new_user)
            db.session.commit()
            flash(f'{new_user.user} successfully created!', 'success')
            return render_template("new_user.html", form=form)
    return render_template("new_user.html", form=form) #"<h1> fart </h1>"

@app.route("/user_records",methods=['GET','POST'])
def user_records():
    return render_template("users.html" ,
        users=User.query.all(),
        title="Show Users"
    )

if __name__ == "__main__":
    app.run(debug=True)