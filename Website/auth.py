from flask import Blueprint, render_template, url_for, redirect, request, flash
from . import db 
from .models import User 
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import logging


auth = Blueprint("auth", __name__)

@auth.route("/profile")
def firstPage():
    return render_template("index.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.firstPage"))

@auth.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        
        #checking duplication of user names and emails
        existing_emails = User.query.filter_by(email=email).first()
        existing_username = User.query.filter_by(username=username).first()
        

        if existing_emails:
            flash('Email is already in use.', category='error')
        elif existing_username:
            flash('Username is already in use.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
        elif len(username) < 2:
            flash('Username is too short.', category='error')
        elif len(password1) < 6:
            flash('Password is too short.', category='error')
        elif len(email) < 6:
            flash('Username is too short.', category='error')
        else:
            #hashing of password created
            new_user = User(email=email, username=username, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash(f'Welcome ' + str(current_user.username))
            return redirect(url_for('views.introduction_posts'))
        

    return render_template("signup.html", user=current_user)

@auth.route("/Login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        logging.basicConfig(filename="demo.log", level=logging.DEBUG)
        if user:
            #matching of hash
            if check_password_hash(user.password, password):
                
                flash("Logged in! ")
                
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Password is incorrect', category='error')
        else:
            flash('Email does not exist', category='error')

    return render_template("login.html", user=current_user)

