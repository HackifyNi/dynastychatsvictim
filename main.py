from flask import Flask, render_template, request
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

        # Using parameterized query to prevent SQL injection
        sql = "INSERT INTO users (fname, lname, dob, username, password) VALUES (%s, %s, %s, %s, %s)"

        

    return render_template('signup.html')


