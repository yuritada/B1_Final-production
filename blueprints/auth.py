from flask import Blueprint, render_template, request, redirect, session
from db import insert_user ,get_user_by_username

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        insert_user('user3', 'password3')
        # execute_query("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        return redirect('/auth/login')
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user_by_username(username)
        # user = fetch_one("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect('/')
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')