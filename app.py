from flask import Flask, render_template, redirect, request, session, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors
from forms import RegisterForm, LoginForm, PostForm
from passlib.hash import sha256_crypt
from datetime import datetime
import json

app = Flask(__name__) #this has 2 underscores on each side
app.secret_key = "&+#kgc^rl=baa_c^cw-db+ij462d%rv*)m+x+jbw*#((()^0^1"

def get_sql_login():
    with open("public/JoshuaTran/python/sqllogin.json", "r") as login:
        return json.load(login)

# Authenticate with MySQL user db
sqllogin = get_sql_login()
app.config["MYSQL_HOST"] = sqllogin.get("host")
app.config["MYSQL_USER"] = sqllogin.get("user")
app.config["MYSQL_PASSWORD"] = sqllogin.get("password")
app.config["MYSQL_DB"] = sqllogin.get("db")
mysql = MySQL(app)

# Thanks to https://www.geeksforgeeks.org/login-and-registration-project-using-flask-and-mysql/

@app.route("/home", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def home():
    # Create cursor
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Get all posts
    cursor.execute("SELECT * FROM joshtran_cheeps_posts ORDER BY date_created DESC")
    posts = cursor.fetchall()

    if request.method == "POST":
        form = PostForm(request.form)
        if form.validate():
            # Get form data
            word = form.word.data
            date_created = datetime.now().strftime('%Y-%m-%d %H:%M:%S') # Get date and format for MySQL

            # If user exists
            if session["loggedin"]:
                user = session["username"]
                cursor.execute("INSERT INTO joshtran_cheeps_posts VALUES (NULL, %s, %s, %s)", (user, date_created, word, ))
                mysql.connection.commit()
                return redirect("")
    else:
        form = PostForm()

    return render_template("index.html", form=form, posts=posts)

@app.route("/login", methods=["GET", "POST"])
def login():
    msg = ""
    # If user is authenticated, redirect them to home/wall
    if session.get("loggedin"):
        return redirect("home")

    if request.method == "POST":
        form = LoginForm(request.form)
        if form.validate():
            # Get form data
            username = form.username.data
            password = form.password.data

            # Create cursor
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            # Fetch account
            cursor.execute("SELECT * FROM joshtran_cheeps_user WHERE username = %s", (username, ))
            account = cursor.fetchone()
            if account and sha256_crypt.verify(password, account["password"]):
                session["loggedin"] = True
                session["uid"] = account["uid"]
                session["username"] = account["username"]
                return redirect("")
            else:
                msg = "User not found."
    else:
        form = LoginForm()

    return render_template("login.html", msg=msg, form=form)
  
@app.route("/logout")
def logout():
    session.pop("loggedin", None)
    session.pop("uid", None)
    session.pop("username", None)
    return redirect("login")
  
@app.route("/register", methods=["GET", "POST"])
def register():
    msg = ""
    if request.method == "POST":
        form = RegisterForm(request.form)
        if form.validate():
            # Get form data
            username = form.username.data
            password = sha256_crypt.encrypt(str(form.password1.data))
            email = form.email.data

            # Create cursor
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            # If data is good, insert into user db
            cursor.execute("SELECT * FROM joshtran_cheeps_user WHERE username = %s", (username, ))
            if cursor.fetchone(): # Check if account with username already exists
                msg = "Account already exists"
            else:
                cursor.execute("INSERT INTO joshtran_cheeps_user VALUES (NULL, %s, %s, %s)", (username, email, password, ))
                mysql.connection.commit()
                return redirect("login")
    else:
        form = RegisterForm()

    return render_template("register.html", msg=msg, form=form)

@app.route("/about", methods=["GET", "POST"])
def about():
    msg = ""
    if request.method == "POST":
        try:
            num = int(request.form["num"])
            color = request.form["color"]
            if num >= 1 and num <= 10:
                return render_template("about.html", num=num, color=color)
        except ValueError: # If user did not put in a number
            msg = "Please input a number..."

    num = None
    color = None
    return render_template("about.html", num=num, color=color, msg=msg)
