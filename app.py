from flask import Flask, render_template, g, request, redirect, url_for, session,flash, jsonify
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
import MySQLdb.cursors
import MySQLdb.cursors, re, hashlib
import pymysql
import mysql.connector
from mysql.connector import MySQLConnection, Error
from pymysql.cursors import DictCursor
from flask_login import login_required
import smtplib
from email.mime.text import MIMEText
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import datetime as dt
from datetime import datetime, date, timedelta
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import logging
import celery
from celery.schedules import crontab
import time


app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = '1a2b3c4d5e6d7g8h9i10'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Miera@8310' #Replace ******* with  your database password.
app.config['MYSQL_DB'] = 'my_database'

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='amierah.honey@gmail.com',
    MAIL_PASSWORD='zstg zndv gjye ckno',
    MAIL_DEFAULT_SENDER='amierah.honey@gmail.com'
)

mail = Mail(app)

# Intialize MySQL
mysql = MySQL(app)

def check_due_tasks():
    cur = mysql.connection.cursor()
    student_id = session['student_id']  # Assuming the student ID is stored in the session
    cur.execute("SELECT * FROM tasks WHERE student_id = %s", (student_id,))
    tasks = cur.fetchall()

    for task in tasks:
        task_id, title, name, due_date, student_id = task
        user_email = get_user_email(student_id)

        # Check if the task is due today or overdue
        if due_date <= datetime.now().date():
            send_task_notification(user_email, name, due_date)

    cur.close()
    mysql.connection.commit()

def get_user_email(student_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT email FROM my_table WHERE student_id = %s", (student_id,))
    user_email = cur.fetchone()[0]
    cur.close()
    return user_email

def send_task_notification(email, name):
    msg = Message(f"Task Reminder: {name}", recipients=[email])
    msg.body = f"This is a reminder that the task '{name}' is due on Thursday."
    mail.send(msg)
    print("Sent a daily notification")

@app.route('/', methods=['GET', 'POST'])
def login():
# Output message if something goes wrong...
    print("DAHH MASSUUUUUUKKKK niiiIII!@3")
    # Check if "email" and "password" POST requests exist (user submitted form)
    # if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
    if request.method == 'POST':
        # Create variables for easy access
        email = request.form['email']
        password = request.form['password']
        print("dapat masuk db dah ni")
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM my_table WHERE email = %s AND password = %s', (email, password))
        # Fetch one record and return result
        print("ni dpt cursor pun dpt gakkHGDs")
        row = cursor.fetchone()
        print("cursor fetchone masukkkkkdsfd")
        print(email)
        print(row)
                # If account exists in accounts table in out database
        if row:
            session['email'] = email
            session['name'] = row['name']
            # Create session data, we can access this data in other routes

            # Retrieve student ID
            student_id = row['student_id']

            # Retrieve the course code associated with the student ID
            cursor.execute('SELECT * FROM courses WHERE student_id = %s', (student_id,))
            details = cursor.fetchone()

            # Store the course data in the session
            session['details'] = details

            return redirect(url_for('dashboard'))
        
        else:
            # Account doesnt exist or email/password incorrect

            flash("Incorrect email/password!", "danger")
            return render_template('./main.html' , row=row)
    print("ni dah lastttt skali ni ha")
    return render_template('./main.html', row=None)


@app.route('/dashboard', methods=['GET', 'POST']) 
def dashboard():
        if 'email' in session and 'name' in session:
            email = session['email']
            name = session['name']

            # Retrieve the details from the session
            details = session.get('details')

            # Check if details are available
            if details:    
                return render_template('./Ulearndash.html', email=email, name=name, details=details)
            else:
                # Redirect to the login page if course_data is not available
                return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))
 

@app.route('/mycourses', methods=['GET'])
def mycourses():
    if request.method == 'GET':
        courses = []
        if 'email' in session:
            student_email = session['email']
            try:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("SELECT c.name, c.code, c.faculty, c.semester, c.lecturer "
                              "FROM courses c "
                              "JOIN my_table mt ON c.student_id = mt.student_id "
                              "WHERE mt.email = %s", (student_email,))
                courses = cursor.fetchall()
                print("heeeee665")
                print(courses)
            except Exception as e:
                print(f"Error fetching courses: {e}")
        return render_template('./courses.html', courses=courses)
    else:
        # Handle other HTTP methods (e.g., POST, PUT, DELETE) if needed
        return 'Method not allowed', 405

@app.route('/learnflow', methods=['GET', 'POST'])
def learnflow():
    email = session.get('email')
    name = session.get('name')
    send_task_notification(email, name)
    print("testing for the email")
    if 'name' not in session:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT phone, email FROM my_table WHERE name = %s", (session['name'],))
    user_info = cursor.fetchone()
    has_phone = user_info[0] is not None

    # Fetch the options for the code and name dropdowns
    cursor.execute("SELECT code FROM courses")
    course_options = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT name FROM courses")
    name_options = [row[0] for row in cursor.fetchall()]

    # Check if the user has submitted the form ()
    if request.method == 'POST':
        if 'phone' in request.form:
            return render_template('./learnflow.html', has_phone=has_phone)
        #     phone_number = request.form['phone']

        code = request.form['code']
        name = request.form['name']
        title = request.form['title']
        description = request.form['description']
        due_date = request.form['due_date']
        # progress = request.form['progress']
        student_id = session['student_id']
        cursor.execute("INSERT INTO tasks (code, name, title, description, due_date, student_id) VALUES ( %s, %s, %s, %s, %s, %s)",
                       (code, name, title, description, due_date,student_id))
        mysql.connection.commit()

        cursor.execute("SELECT title, name, code, due_date, progress FROM tasks WHERE student_id = (SELECT student_id FROM my_table WHERE name = %s)", (session['name'],))
        tasks = cursor.fetchall()
        print("TRY TENGOK")
        print(tasks)
    else:
        cursor.execute("SELECT title, name, code, due_date, progress FROM tasks WHERE student_id = (SELECT student_id FROM my_table WHERE name = %s)", (session['name'],))
        tasks = []
        today = datetime.now().date()
        print(today)
        for title, name, code, due_date, progress in cursor.fetchall():
            if isinstance(due_date, date):
                days_remaining = (due_date - today).days
                tasks.append({
                    'name': name,
                    'code': code,
                    'title': title,
                    'days_remaining': days_remaining,
                    'progress': progress,
                })
                print(days_remaining)
            else:
                tasks.append({
                    'name': name,
                    'code': code,
                    'title': title,
                    'days_remaining': None,
                    'progress': progress,
                })

        # cursor.execute("SELECT code, name FROM courses WHERE student_id = (SELECT student_id FROM my_table WHERE name = %s)", (session['name'],))
        # coursess = cursor.fetchall()

    code = request.args.get('code')
    if code:
        cursor.execute("SELECT * FROM courses WHERE code = %s", (code,))
        course = cursor.fetchone()
        if course:
            return render_template('./learnflow.html', course=course, user_info=user_info, has_phone=has_phone, tasks=tasks, course_options=course_options, name_options=name_options)
        else:
            return 'Course not found', 404
    else:
        cursor.execute("SELECT c.* FROM courses c JOIN my_table mt ON c.student_id = mt.student_id WHERE mt.name = %s LIMIT 1", (session['name'],))
        course = cursor.fetchone()
        if course:
            cursor.execute("SELECT title, name, code, due_date, progress FROM tasks WHERE student_id = (SELECT student_id FROM my_table WHERE name = %s)", (session['name'],))
            tasks = []
            today = datetime.now().date()
            for title, name, code, due_date, progress in cursor.fetchall():
                if isinstance(due_date, date):
                    days_remaining = (due_date - today).days
                    tasks.append({
                        'name': name,
                        'code': code,
                        'title': title,
                        'days_remaining': days_remaining,
                        'progress': progress,
                    })
                else:
                    tasks.append({
                        'name': name,
                        'code': code,
                        'title': title,
                        'days_remaining': None,
                        'progress': progress,
                    })



            return render_template('./learnflow.html', course=course, user_info=user_info, has_phone=has_phone, tasks=tasks, course_options=course_options, name_options=name_options)
        else:
            return 'No courses found', 404

def send_email_notification(recipient_email, subject, body):
    msg = Message(
        subject=subject,
        recipients=[recipient_email]
    )
    msg.body = body
    mail.send(msg)
    print("Sent a daily notification")

# def send_sms_notification(recipient_phone, message):
#     print("INI NUMBER I")
#     print(recipient_phone)
#     try:
#         account_sid = 'AC69ed5fb90250f9e959dd996a8a5b2838'
#         auth_token = '5e73ce5e62feb5b9f5502c48cd379d84'
#         client = Client(account_sid, auth_token)

#         client.messages.create(
#             body=message,
#             from_='+16168187028',
#             to=recipient_phone
#         )
#     except TwilioRestException as e:
#         # Log the error and provide more information
#         app.logger.error(f"Error sending SMS notification to {recipient_phone}: {e}")
#         app.logger.error(f"Error details: {e.msg}")
#         # You can also raise a custom exception or return an error message to the user
#         raise Exception("Error sending SMS notification. Please try again later.")
#     except Exception as e:
#         # Log any other unexpected errors
#         app.logger.error(f"Unexpected error sending SMS notification to {recipient_phone}: {e}")
#         raise Exception("Error sending SMS notification. Please try again later.")



@app.route('/add_schedule', methods=['POST'])
def add_schedule():
    course_code = request.form['course_code']
    name = request.form['name']
    title = request.form['title']
    description = request.form['description']
    due_date = request.form['due_date']

    # Insert the new task into the database
    conn = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (student_id,course_code, name, title,description, due_date) VALUES (%s, %s, %s, %s, %s, %s)", (session['student_id'], course_code, name, title, description, due_date))
    conn.commit()
    cursor.close()
    conn.close()


    # Redirect to the LearnFlow page
    return redirect(url_for('learnflow'), tasks=tasks)

@app.route('/get_course_data', methods=['GET'])
def get_course_data(code):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT code, name FROM courses")
    courses = cursor.fetchall()
    course_codes = [course['code'] for course in courses]
    course_names = [course['name'] for course in courses]
    return course_codes, course_names


@app.route('/update-task/<int:task_id>', methods=['POST'])
def update_task(task_id):
    # Find the task in the list based on the task_id
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404

    # Update the task details based on the request data
    data = request.get_json()
    task['title'] = data['title']
    task['progress'] = data['progress']

    # Save the updated task to the list or database
    # ...

    return jsonify({'message': 'Task updated successfully'})

def send_email_notification(recipient_email, subject, body):
    try:
        msg = Message(subject, sender='amierah.honey@gmail.com', recipients=[recipient_email])
        msg.body = body
        mail.send(msg)
        print("Email sent successfully!")
    except Exception as e:
        print("Error sending email:", e)



@app.route('/save-schedule', methods=['POST'])
def save_schedule():
    # Get the form data from the request
    course_code = request.json['courseCode']
    course_name = request.json['courseName']
    title = request.json['title']
    description = request.json['description']
    due_date_str = request.json['dueDate']
    if due_date_str:
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        days_remaining = (due_date - datetime.now().date()).days
    else:
        due_date = None
        days_remaining = None

    recipient_email = session['email']

    # Send the initial notification
    subject=f"New Task: {course_code} - {course_name} - {title}"
    body = f"A new task, '{title}', for {course_code} - {course_name} has been created with a due date of {due_date.strftime('%Y-%m-%d')}."
    send_email_notification(recipient_email,subject, body)
    print("NI DAH DAPAT HANTAR EMAIL ")
    return jsonify({
        'courseCode': course_code,
        'courseName': course_name,
        'title': title,
        'description': description,
        'dueDate': due_date.strftime('%Y-%m-%d') if due_date else None,
        'daysRemaining': days_remaining
    })
    return course_code, course_name, title, description, due_date, days_remaining


@app.route('/course/<course_code>')
def course_detail(course_code):
    # Fetch the details of the specific course
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM courses WHERE code = %s", (course_code,))
    course = cursor.fetchone()
    print("here's the selected course")
    print(course)
    if course:
        return render_template('coursedash.html', course=course)
    else:
        return 'Course not found', 404


@app.route('/task1')
def task1():
    # Fetch the details of the specific course
    course_code = request.args.get('course_code')
    if course_code:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM courses WHERE code = %s", (course_code,))
        course = cursor.fetchone()
        print("here's the selected course")
        print(course)
        if course:
            return render_template('task1.html', course=course)
        else:
            return 'Course not found', 404
    else:
        return 'Course code not provided', 400 


# Schedule the daily task check
scheduler = BackgroundScheduler()
scheduler.add_job(check_due_tasks, trigger=CronTrigger(hour=18, minute=5))
scheduler.start()



if __name__ =='__main__':
	app.run(debug=True)