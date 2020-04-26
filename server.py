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


@app.route('/register_event')
def reg_valid():
    if 'user_id' not in session:
        return redirect('/')
    mysql = connectToMySQL('event_manager')
    query = "SELECT * FROM student_accounts WHERE id = %(id)s;"
    data = {'id': session['user_id']}
    reg_user = mysql.query_db(query, data)
    mysql = connectToMySQL('event_manager')
    query = "SELECT id, event_name, start_date, host FROM events WHERE id NOT IN (SELECT event_id FROM event_participants WHERE student_account_id = %(uid)s)"
    data = {'uid': session['user_id']}
    reg_events = mysql.query_db(query, data)
    if reg_user and reg_user[0]['id'] == session['user_id']:
        return render_template("register_event.html", events=reg_events)
    return redirect('/success')


@app.route('/update_acct/<user_id>')
def account_valid(user_id):
    if 'user_id' not in session:
        return redirect('/')
    mysql = connectToMySQL('event_manager')
    query = "SELECT * FROM student_accounts WHERE id = %(id)s"
    data = {'id': session['user_id']}
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
    query = "SELECT * FROM student_accounts WHERE id = %(id)s;"
    data = {'id': session['user_id']}
    st_acct = mysql.query_db(query, data)
    mysql = connectToMySQL('event_manager')
    query = "SELECT * FROM event_participants WHERE student_account_id = %(id)s;"
    data = {'id': session['user_id']}
    st_events = mysql.query_db(query, data)
    return render_template("student_dashboard.html",  st_acct=st_acct, st_events=st_events)


@app.route('/reg_event/<id>')
def add_regevent(id):
    if 'user_id' not in session:
        return redirect('/')
    mysql = connectToMySQL('event_manager')
    query = "INSERT INTO studentacct_event (student_account_id, event_id, created_at, updated_at) VALUES (%(student)s, %(event)s, NOW(),NOW())"
    data = {'student': session['user_id'], 'event': int(id)}
    eventreg = mysql.query_db(query, data)
    mysql = connectToMySQL('event_manager')
    query = "INSERT INTO event_participants(event, student_account_id, event_id, date_time, host, notes, created_at, updated_at) SELECT events.event_name, %(student)s, events.id, events.start_date, events.host, events.notes, NOW(), NOW() FROM events WHERE events.id=%(event)s"
    data = {'student': session['user_id'], 'event': int(id)}
    reg_tbl = mysql.query_db(query, data)
    return redirect("/success")


# @app.route('/like/<id>')
# def add_like(id):
#     mysql = connectToMySQL('event_manager')
#     query = "UPDATE quotes SET likes = likes + 1 WHERE id = %(quote_id)s"
#     data = {'quote_id': (id)}
#     result = mysql.query_db(query, data)
#     return redirect('/success')


# @app.route('/user/<id>')
# def user_quotes(id):
#     if 'user_id' not in session:
#         return redirect('/')
#     mysql = connectToMySQL('event_manager')
#     query = "SELECT id, first_name, last_name FROM users WHERE id = %(user_id)s"
#     data = {'user_id': session['user_id']}
#     user = mysql.query_db(query, data)
#     mysql = connectToMySQL('event_manager')
#     query = "SELECT quotes.user_id AS 'usrID', quotes.author AS 'author', quotes.quote AS 'quote', users.first_name AS 'first_name', users.last_name AS 'last_name' FROM quotes JOIN users ON quotes.user_id = users.id WHERE user_id = %(user_id)s"
#     data = {'user_id': int(id)}
#     quotes = mysql.query_db(query, data)
#     return render_template("user_quotes.html", user=user, quotes=quotes)


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
        if len(request.form['int_fb']) < 1:
            flash("Please enter your Facebook API Key.")
            is_valid = False
        if len(request.form['int_tw']) < 1:
            flash("Please enter your Twitter API Key.")
            is_valid = False
        if is_valid:
            mysql = connectToMySQL('event_manager')
            query = "UPDATE student_accounts SET school_name = %(schname)s, first_name = %(fname)s, last_name = %(lname)s, email = %(email)s, phone_number = %(phone)s, int_fb = %(fb)s, int_tw = %(tw)s, updated_at = NOW() WHERE id = %(user_id)s"
            data = {
                'schname': request.form['school_name'],
                'fname': request.form['first_name'],
                'lname': request.form['last_name'],
                'email': request.form['email'],
                'phone': request.form['phone_number'],
                'fb': request.form['int_fb'],
                'tw': request.form['int_tw'],
                'user_id': session['user_id']
            }
            mysql = mysql.query_db(query, data)
        else:
            return redirect(f'/myaccount/{user_id}')
        return redirect('/success')


@app.route('/cancel/<id>')
def cancel_reg(id):
    mysql = connectToMySQL('event_manager')
    query = "SELECT * FROM student_accounts WHERE id = %(id)s"
    data = {'id': session['user_id']}
    cancel_event_reg = mysql.query_db(query, data)
    if cancel_event_reg and cancel_event_reg[0]['id'] == session['user_id']:
        mysql = connectToMySQL('event_manager')
        query = "DELETE FROM event_participants WHERE id = %(event_part)s;"
        data = {'event_part': int(id)}
        del_reg = mysql.query_db(query, data)
    return redirect("/success")


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
