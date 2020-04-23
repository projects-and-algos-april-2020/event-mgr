from flask import Flask, render_template, request, redirect, session, flash
from flask_bcrypt import Bcrypt
import re
from datetime import datetime
from mysqlconnection import connectToMySQL

app = Flask(__name__)
app.secret_key = 'My name is CJ and I quit'
bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


@app.route('/')
def index():
        return render_template("index.html")


@app.route('/register_event/<user_id>')
def reg_valid(user_id):
    if 'user_id' not in session:
        return redirect('/')
    mysql = connectToMySQL('event_manager')
    query = "SELECT * FROM student_accounts WHERE id = %(id)s;"
    data = {'id': session['user_id']}
    reg_user = mysql.query_db(query, data)
    mysql = connectToMySQL('event_manager')
    query = "SELECT * FROM events WHERE start_date > NOW();"
    data = {'id': session['user_id']}
    reg_events = mysql.query_db(query, data)
    if reg_user and reg_user[0]['id'] == session['user_id']:
        return render_template("register_cancel_event.html", events=reg_events)
    return redirect('/success')


@app.route('/update_acct/<user_id>')
def account_valid(user_id):
    if 'user_id' not in session:
        return redirect('/')
    mysql = connectToMySQL('event_manager')
    query = "SELECT * FROM student_accounts WHERE id = %(user_id)s"
    data = {'user_id': session['user_id']}
    this_user = mysql.query_db(query, data)
    if this_user and this_user[0]['id'] == session['user_id']:
        return render_template("update_student_acct.html", user=this_user[0])   
    return redirect('/success')


@app.route('/save_user', methods=['POST'])
def add_user():
    is_valid = True     # assume True
    if len(request.form['school_name']) < 2:
        flash("Please enter a school name at least 2 characters long.")
        is_valid = False
    if len(request.form['first_name']) < 2:
        flash("Please enter a first name at least 2 characters long.")
        is_valid = False
    if not request.form['first_name'].isalpha():
        flash("First name must contain letters only.")
        is_valid = False
    if len(request.form['last_name']) < 2:
        flash("Please enter a last name at least 2 characters long.")
        is_valid = False
    if not request.form['last_name'].isalpha():
        flash("Last name must contain letters only.")
        is_valid = False
    if len(request.form['email']) < 1:
        flash("Please enter your email address.")
        is_valid = False
    if not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid email, please enter email address again.")
        is_valid = False
#  add validation that email submitted is not in the database
#  flag as false if in the database
    mysql = connectToMySQL('event_manager')
    query = "SELECT * FROM student_accounts WHERE email = %(email)s;"
    data = {"email": request.form["email"]}
    result = mysql.query_db(query, data)
    if result:
        flash("Email address is already in use.")
        is_valid = False
    if len(request.form['password']) < 5:
        flash("Password should be at least 5 characters.")
        is_valid = False
    if (request.form['password']) != (request.form['passwordcon']):
        flash("Password and password confirmation must be identical.")
        is_valid = False
    if not is_valid:
        return redirect('/')
    if is_valid:
        mysql = connectToMySQL('event_manager')
        query = "INSERT INTO student_accounts (school_name, first_name, last_name, email, password, created_at, updated_at) VALUES (%(school)s,%(fn)s, %(ln)s, %(em)s, %(password_hash)s, NOW(), NOW())"
        data = {
            'school': request.form['school_name'],
            'fn': request.form['first_name'],
            'ln': request.form['last_name'],
            'em': request.form['email'],
            'password_hash': bcrypt.generate_password_hash(request.form['password'])
        }
        result = mysql.query_db(query, data)
        print(result)
        flash("Registration was successful. Please login.")
    return redirect('/')


@app.route('/login', methods=['POST'])
def login():
    is_valid = True
    if len(request.form['email']) < 2:
        is_valid = False
        flash("Please re-enter your email")
    if len(request.form['password']) < 2:
        is_valid = False
        flash("Please re-enter your password")
    if not is_valid:
        return redirect('/')
    else:
        mysql = connectToMySQL('event_manager')
        query = "SELECT * FROM student_accounts WHERE email = %(email)s;"
        data = {'email': request.form['email'],
                'password': request.form['password']}
        result = mysql.query_db(query, data)
        if result:
            if bcrypt.check_password_hash(result[0]['password'], request.form['password']):
                session['user_id'] = result[0]['id']
                session['first_name'] = result[0]['first_name']
                session['last_name'] = result[0]['last_name']
                return redirect('/success')
        flash('You could not be logged in. Please try again.')
    return redirect('/')


@app.route('/success')
def ifgood():
    if 'user_id' not in session:
        return redirect('/')
    mysql = connectToMySQL('event_manager')
    query = "SELECT * FROM student_accounts WHERE id = %(user_id)s;"
    data = {"user_id": session["user_id"]}
    st_acct = mysql.query_db(query, data)
    mysql = connectToMySQL('event_manager')
    query = "SELECT events.event_name, events.start_date, events.host, events.notes FROM events JOIN studentacct_event ON events.id=studentacct_event.event_id WHERE start_date > NOW() AND studentacct_event.student_account_id = %(id)s;"
    data = {'id': session['user_id']}
    student_events = mysql.query_db(query,data)
    return render_template("student_dashboard.html", events=student_events, st_acct=st_acct)


@app.route('/reg_event', methods=['POST'])
def add_reg():
    is_valid = True
    if len(request.form['author']) < 4:
        is_valid = False
        flash('Author must be at least 4 characters long.')
    if len(request.form['quote']) < 11:
        is_valid = False
        flash('Quote must be at least 11 characters long.')
    if is_valid:
        mysql = connectToMySQL('event_manager')
        query = "INSERT INTO quotes (user_id, author, quote, created_at, updated_at) VALUES (%(user_id)s, %(author)s, %(quote)s, NOW(), NOW())"
        data = {"author": request.form["author"],
                "quote": request.form["quote"], "user_id": session["user_id"]}
        mysql = mysql.query_db(query, data)
    return redirect("/success")


@app.route('/like/<id>')
def add_like(id):
    mysql = connectToMySQL('event_manager')
    query = "UPDATE quotes SET likes = likes + 1 WHERE id = %(quote_id)s"
    data = {'quote_id': (id)}
    result = mysql.query_db(query, data)
    return redirect('/success')


@app.route('/user/<id>')
def user_quotes(id):
    if 'user_id' not in session:
        return redirect('/')
    mysql = connectToMySQL('event_manager')
    query = "SELECT id, first_name, last_name FROM users WHERE id = %(user_id)s"
    data = {'user_id': session['user_id']}
    user = mysql.query_db(query, data)
    mysql = connectToMySQL('event_manager')
    query = "SELECT quotes.user_id AS 'usrID', quotes.author AS 'author', quotes.quote AS 'quote', users.first_name AS 'first_name', users.last_name AS 'last_name' FROM quotes JOIN users ON quotes.user_id = users.id WHERE user_id = %(user_id)s"
    data = {'user_id': int(id)}
    quotes = mysql.query_db(query, data)
    return render_template("user_quotes.html", user=user, quotes=quotes)


@app.route('/myaccount/<user_id>', methods=['POST'])
def edit_myaccount(user_id):
    mysql = connectToMySQL('event_manager')
    query = "SELECT * FROM student_accounts WHERE id = %(user_id)s"
    data = {"user_id": session["user_id"]}
    edit_user = mysql.query_db(query, data)
    if edit_user and edit_user[0]['id'] == session['user_id']:
        is_valid = True
        if len(request.form['school_name']) < 2:
            flash("Please enter a school name at least 2 characters long.")
            is_valid = False
        if len(request.form['first_name']) < 2:
            flash("Please enter a first name at least 2 characters long.")
            is_valid = False
        if not request.form['first_name'].isalpha():
            flash("First name must contain letters only.")
            is_valid = False
        if len(request.form['last_name']) < 2:
            flash("Please enter a last name at least 2 characters long.")
            is_valid = False
        if not request.form['last_name'].isalpha():
            flash("Last name must contain letters only.")
            is_valid = False
        if len(request.form['email']) < 1:
            flash("Please enter your email address.")
            is_valid = False
        if not EMAIL_REGEX.match(request.form['email']):
            flash("Invalid email, please enter email address again.")
            is_valid = False
        if len(request.form['phone_number']) < 1:
            flash("Please enter your phone number.")
            is_valid = False
        if is_valid:
            mysql = connectToMySQL('event_manager')
            query = "UPDATE student_accounts SET school_name = %(schname)s, first_name = %(fname)s, last_name = %(lname)s, email = %(email)s, phone_number = %(phone)s, updated_at = NOW() WHERE id = %(user_id)s"
            data = {
                'schname': request.form['school_name'],
                'fname': request.form['first_name'],
                'lname': request.form['last_name'],
                'email': request.form['email'],
                'phone': request.form['phone_number'],
                'user_id': session['user_id']
            }
            mysql = mysql.query_db(query, data)
        else:
            return redirect(f'/myaccount/{user_id}')
        return redirect('/success')


@app.route('/delete/<id>')
def del_acct(id):
    mysql = connectToMySQL('event_manager')
    query = "SELECT * FROM student_accounts WHERE id = %(user_id)s"
    data = {"user_id": session["user_id"]}
    del_acct = mysql.query_db(query, data)
    if del_acct and del_acct[0]['id'] == session['user_id']:
        mysql = connectToMySQL('event_manager')
        query = "DELETE FROM student_accounts WHERE student_account_id = %(id)s AND id = %(id)s"
        data = {'id': session['user_id'], 'student_account_id': session[id]}
        mysql = mysql.query_db(query, data)
    return redirect("/success")


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
