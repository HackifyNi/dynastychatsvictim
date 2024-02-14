from flask import Flask, render_template, request, redirect, url_for
import flask_login
import pymysql
import pymysql.cursors
from datetime import datetime

app = Flask(__name__)

app.secret_key = "thisisthesupersecretpassworddonttellnobody"


login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class User:
    is_authenticated = True
    is_anonymous = False
    is_active = True
    def __init__(self, id, username, pfp):
        self.id = id
        self.username = username
        self.pfp = pfp
    def get_id(self):
        return str(self.id)
    
    
class User(flask_login.UserMixin):
    def __init__(self, user_id, username, pfp):
        self.id = user_id
        self.username = username
        self.pfp = pfp

    def get_id(self):
        return str(self.id)

    def get_posts(self):
        cursor = conn.cursor()
        cursor.execute(f"SELECT Posts.*, users.username as username FROM `Posts`")
        posts = cursor.fetchall()
        cursor.close()
        return posts

        


conn = pymysql.connect(
    host='10.100.33.60',
    user='cjohn',
    password='224257683',
    database='cjohn_dynasty',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

@login_manager.user_loader

def load_user(user_id):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM `users` WHERE `id` = ' + str(user_id))
    result = cursor.fetchone()
    cursor.close()
    conn.commit()
    if result is None:
        return None
    return User(result["id"],result["pfp"],result["username"])

@app.route('/')
def index():
    if flask_login.current_user.is_authenticated:
        return redirect('/feed')
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

        
        return redirect('/login')
    if flask_login.current_user.is_authenticated:
        return redirect('/feed')
   

    return render_template('signup.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM `users` WHERE username='{username}'")
        result = cursor.fetchone()
        if result and result['password'] == password:
            user = load_user(result["id"])
            flask_login.login_user(user)
            return redirect('/feed')
        else:
            error= "Invalid username or password. Please try again."
            return render_template('login.html', error=error)
    if flask_login.current_user.is_authenticated:
        return redirect('/feed')
    
    return render_template('login.html')



@app.route('/feed', methods=['GET', 'POST'])
@flask_login.login_required
def post_feed():
    if request.method == 'POST':
        user_id = flask_login.current_user.id
        likes = 0  
        description = request.form['description']
        image = request.form['image'] 
        timestamp = datetime.now()

        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO `Posts` (user_id, likes, description, image, timestamp) "
            f"VALUES ({user_id}, {likes}, '{description}', '{image}', '{timestamp}')"
        )
        cursor.close()
        conn.commit()

    cursor = conn.cursor()
    cursor.execute("SELECT * from `Posts` JOIN `users` ON Posts.user_id = users.id ORDER BY `timestamp`")
    result = cursor.fetchall()
    return render_template('feed.html.jinja', posts=result)



@app.route('/debug_posts')
@flask_login.login_required
def debug_posts():
    user_posts = flask_login.current_user.get_posts()
    print(user_posts)   
    return render_template('debug_posts.html.jinja', posts=user_posts)


