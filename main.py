from flask import Flask, render_template, request, redirect, url_for
import pymysql
import pymysql.cursors

app = Flask(__name__)

conn = pymysql.connect(
    host='10.100.33.60',
    user='cjohn',
    password='224257683',
    database='cjohn_dynasty',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

@app.route('/')
def index():
    return render_template('landing.html.jinja')



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        fname = request.form['first_name']
        lname = request.form['last_name']
        dob = request.form['birthday']
        username = request.form['username']
        password = request.form['password']

        cursor = conn.cursor()

        cursor.execute(f"INSERT INTO `users` (fname, lname, dob, username, password) VALUES ('{fname}', '{lname}', '{dob}', '{username}', '{password}')")
        cursor.close()
        conn.commit()
        
        return redirect(url_for('login'))

    return render_template('signup.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM `users` WHERE username='{username}'")
        user = cursor.fetchone()
        if user and user['password'] == password:
            return redirect('/feed')
        else:
            error= "Invalid username or password. Please try again."
            return render_template('login.html', error=error)

    return render_template('login.html')

@app.route('/feed')
def feed():
    return "Hello World"


