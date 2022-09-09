# flask imports
from celery.schedules import crontab
from flask_celery import make_celery
import subprocess
import pydf
from headless_pdfkit import generate_pdf
from httplib2 import Http
from json import dumps
import os
from flask_mail import Mail, Message
import pdfkit
import flask_excel as excel
from flask_cors import CORS
from functools import wraps
from datetime import datetime, timedelta
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
import uuid  # for public id
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify, make_response, render_template, url_for, redirect
from sqlite3 import Timestamp
from distutils.log import Log
import math
import random
from email.policy import default
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("agg")
# imports for PyJWT authentication


# creates Flask object
app = Flask(__name__)
mail = Mail(app)
CORS(app)

# configuration
# NEVER HARDCODE YOUR CONFIGURATION IN YOUR CODE
# INSTEAD CREATE A .env FILE AND STORE IN IT
app.config['SECRET_KEY'] = 'your secret key'
# database name
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# creates SQLALCHEMY object
db = SQLAlchemy(app)


# Database ORMs
# celery config
app.config['CELERY_BROKER_URL'] = "redis://localhost:6379/0"
app.config['CELERY_BACKEND'] = "redis://localhost:6379/0"
app.config['timezone'] = 'Asia/Kolkata'
app.config['beat_schedule'] = {
    'send-daily-reminder': {
        'task': 'daily_reminder',
        'schedule': crontab(hour=18, minute=00)
    },
    'send-monthly-report': {
        'task': 'monthly_report',
        'schedule': crontab(0, 0, day_of_month='1')
    },
}

celery = make_celery(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(70), unique=True)
    password = db.Column(db.String(80))
    otp = db.Column(db.String(4), default="0")
    joined = db.Column(db.DateTime, nullable=False)
    lastvisit = db.Column(db.DateTime, nullable=False)


class Tracker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    desc = db.Column(db.String(500))
    trackertype = db.Column(db.String(20))
    user_id = db.Column(db.Integer)
    lastused = db.Column(db.DateTime, nullable=False)


class Logs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(500))
    note = db.Column(db.String(500))
    trackerid = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, nullable=False,
                          default=datetime.now())
    user_id = db.Column(db.Integer)

# decorator for verifying the JWT


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query\
                .filter_by(public_id=data['public_id'])\
                .first()
        except:
            return jsonify({
                'message': 'Token is invalid !!'
            }), 401
        # returns the current logged in users contex to the routes
        return f(current_user, *args, **kwargs)

    return decorated

# User Database Route
# this route sends back list of users


@app.route('/user', methods=['GET'])
@token_required
def get_users(current_user):
    output = {}
    output['public_id'] = current_user.public_id
    output['email'] = current_user.email
    output['name'] = current_user.name
    output['joined'] = current_user.joined
    output['lastvisit'] = current_user.lastvisit

    return jsonify({'user': output})
    # querying the database
    # for all the entries in it

    #users = User.query.all()
    # converting the query objects
    # to list of jsons

    # for user in users:
    # appending the user data json
    # to the response list


@app.route('/deleteuser', methods=['DELETE'])
@token_required
def delete_user(current_user):
    user = User.query.filter_by(
        id=current_user.id).first()

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'user deleted!'})


# route for logging user in
@app.route('/login', methods=['POST'])
def login():
    # creates dictionary of form data
    auth = request.get_json()

    if not auth or not auth.get('email') or not auth.get('password'):
        # returns 401 if any email or / and password is missing
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate': 'Basic realm ="Login required !!"'}
        )

    user = User.query\
        .filter_by(email=auth.get('email'))\
        .first()

    if not user:
        # returns 401 if user does not exist
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate': 'Basic realm ="User does not exist !!"'}
        )

    if check_password_hash(user.password, auth.get('password')):
        # generates the JWT Token
        token = jwt.encode({
            'public_id': user.public_id,
            'exp': datetime.utcnow() + timedelta(minutes=30)
        }, app.config['SECRET_KEY'])
        user.lastvisit = datetime.now()

        # insert user
        db.session.add(user)
        db.session.commit()

        return make_response(jsonify({'token': token.decode('UTF-8')}), 201)
    # returns 403 if password is wrong
    return make_response(
        'Could not verify',
        403,
        {'WWW-Authenticate': 'Basic realm ="Wrong Password !!"'}
    )

# signup route


@app.route('/signup', methods=['POST'])
def signup():
    # creates a dictionary of the form data
    data = request.get_json()

    # gets name, email and password
    name, email = data.get('name'), data.get('email')
    password = data.get('password')

    # checking for existing user
    user = User.query\
        .filter_by(email=email)\
        .first()
    if not user:
        # database ORM object
        user = User(
            public_id=str(uuid.uuid4()),
            name=name,
            email=email,
            password=generate_password_hash(password),
            joined=datetime.now(),
            lastvisit=datetime.now()
        )
        # insert user
        db.session.add(user)
        db.session.commit()

    # generates the JWT Token
        token = jwt.encode({
            'public_id': user.public_id,
            'exp': datetime.utcnow() + timedelta(minutes=30)
        }, app.config['SECRET_KEY'])

        return make_response(jsonify({'token': token.decode('UTF-8')}), 201)

        # return make_response("successfully registerd.", 201)
    else:
        # returns 202 if user already exists
        return make_response('User already exists. Please Log in.', 202)


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'saurabhsatapathy0@gmail.com'
app.config['MAIL_PASSWORD'] = 'btnntitvmzccqwzw'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

# function to generate OTP


def generateOTP():

    # Declare a digits variable
    # which stores all digits
    digits = "0123456789"
    OTP = ""

   # length of password can be changed
   # by changing value in range
    for i in range(4):
        OTP += digits[math.floor(random.random() * 10)]

    return OTP


@celery.task(name='daily_reminder')
def daily_reminder():
    with app.app_context():
        """Hangouts Chat incoming webhook quickstart."""
        url = "https://chat.googleapis.com/v1/spaces/AAAAAtSYpgM/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=r9rrtZ3RiRphmV6mzFu8utJDZaOqytGyOnQveR8OMHQ%3D"
        bot_message = {
            'text': 'Hurry up!!! Track Something now.'}
        message_headers = {'Content-Type': 'application/json; charset=UTF-8'}
        http_obj = Http()
        response = http_obj.request(
            uri=url,
            method='POST',
            headers=message_headers,
            body=dumps(bot_message),
        )
        print(response)
        users = User.query.filter_by().all()
        rec = []
        for user in users:
            if ((datetime.now()-user.lastvisit).days <= 24):
                rec.append(user.email)
        msg2 = Message(
            "Hurry Up!! Track something Now. -quansApp Reminder",
            sender='saurabhsatapathy0@gmail.com',
            recipients=rec
        )

        msg2.body = 'Hello, '+user.name + \
            '\nWe have noticed that you have not tracked anything in last 24 hours!! Track something Now.  '
        mail.send(msg2)


@app.route("/<email>/generateotp", methods=['GET'])
def index(email):

    user = User.query\
        .filter_by(email=email)\
        .first()

    if not user:
        return make_response('No user exist', 401)

    OTP = generateOTP()
    msg = Message(
        OTP+"-quansApp OTP",
        sender='saurabhsatapathy0@gmail.com',
        recipients=[email]
    )
    msg.body = 'Hello, Your quansApp password reset OTP is '+OTP
    mail.send(msg)
    user.otp = OTP
    db.session.add(user)
    db.session.commit()
    return make_response(user.otp+OTP, 201)


@app.route("/resetpassword", methods=['POST'])
def resetpassword():
    data = request.get_json()
    user = User.query\
        .filter_by(email=data.get('email'))\
        .first()
    if not user:
        return make_response('No user exist', 401)
    if (user.otp == data.get('otp')):
        user.otp = "0"
        password = data.get('password')
        user.password = generate_password_hash(password)
        db.session.add(user)
        db.session.commit()
        return make_response("password changed", 201)
    return make_response("not changed something wrong", 400)


@app.route('/addtracker', methods=['POST'])
@token_required
def create_tracker(current_user):
    data = request.get_json()

    new_tracker = Tracker(name=data['name'], desc=data['desc'],
                          trackertype=data['trackertype'], user_id=current_user.id, lastused=datetime.now())
    db.session.add(new_tracker)
    db.session.commit()

    return jsonify({'message': "Tracker created!"})


@app.route('/trackers', methods=['GET'])
@token_required
def get_all_trackers(current_user):
    trackers = Tracker.query.filter_by(user_id=current_user.id).all()

    output = []

    for tracker in trackers:
        tracker_data = {}
        tracker_data['id'] = tracker.id
        tracker_data['name'] = tracker.name
        tracker_data['desc'] = tracker.desc
        tracker_data['trackertype'] = tracker.trackertype
        tracker_data['lastused'] = tracker.lastused
        output.append(tracker_data)

    return jsonify({'trackers': output})


@app.route('/delalltrackers', methods=['DELETE'])
@token_required
def del_all_trackers(current_user):
    trackers = Tracker.query.filter_by(user_id=current_user.id).all()
    logs = Logs.query.filter_by(
        user_id=current_user.id).all()
    for log in logs:
        db.session.delete(log)
        db.session.commit()

    for tracker in trackers:
        db.session.delete(tracker)
        db.session.commit()

    return jsonify({'message': 'all trackers deleted'})


@app.route('/deltracker/<tracker_id>', methods=['DELETE'])
@token_required
def delete_tracker(current_user, tracker_id):
    tracker = Tracker.query.filter_by(
        id=tracker_id, user_id=current_user.id).first()
    logs = Logs.query.filter_by(
        user_id=current_user.id, trackerid=tracker.id).all()

    for log in logs:
        db.session.delete(log)
        db.session.commit()

    if not tracker:
        return jsonify({'message': 'No tracker found!'})

    db.session.delete(tracker)
    db.session.commit()

    return jsonify({'message': 'Trakcer deleted!'})


@app.route('/updatetracker/<tracker_id>', methods=['POST'])
@token_required
def update_tracker(current_user, tracker_id):
    tracker = Tracker.query.filter_by(
        id=tracker_id, user_id=current_user.id).first()

    if not tracker:
        return jsonify({'message': 'No tracker found!'})

    data = request.get_json()
    tracker.name = data["name"]
    tracker.desc = data["desc"]
    tracker.trackertype = data["trackertype"]
    db.session.add(tracker)
    db.session.commit()
    return jsonify({'message': 'Trakcer updated!'})


@app.route('/<tracker_id>/log', methods=['POST'])
@token_required
def create_log(current_user, tracker_id):
    data = request.get_json()

    new_log = Logs(value=data['value'], note=data['note'],
                   user_id=current_user.id, trackerid=tracker_id)
    db.session.add(new_log)
    db.session.commit()
    tracker = Tracker.query.filter_by(
        id=tracker_id, user_id=current_user.id).first()
    tracker.lastused = datetime.now()
    db.session.add(tracker)
    db.session.commit()

    return jsonify({'message': "new log added"})


@app.route('/<tracker_id>/alllog', methods=['GET'])
@token_required
def get_all_logs(current_user, tracker_id):
    logs = Logs.query.filter_by(
        user_id=current_user.id, trackerid=tracker_id).all()

    output = []

    for log in logs:
        log_data = {}
        log_data['id'] = log.id
        log_data['trackerid'] = log.trackerid
        log_data['note'] = log.note
        log_data['value'] = log.value
        log_data['timestamp'] = log.timestamp
        output.append(log_data)

    return jsonify({'logs': output})


@app.route('/<tracker_id>/delalllogs', methods=['DELETE'])
@token_required
def del_all_logs(current_user, tracker_id):
    logs = Logs.query.filter_by(
        user_id=current_user.id, trackerid=tracker_id).all()

    for log in logs:
        db.session.delete(log)
        db.session.commit()

    return jsonify({'message': 'All trackers deleted'})


@app.route('/deletelog/<tracker_id>/<log_id>', methods=['DELETE'])
@token_required
def delete_log(current_user, log_id, tracker_id):
    log = Logs.query.filter_by(
        id=log_id, user_id=current_user.id, trackerid=tracker_id).first()

    if not log:
        return jsonify({'message': 'No todo found!'})

    db.session.delete(log)
    db.session.commit()

    return jsonify({'message': 'Todo item deleted!'})


@app.route('/tracker/<tracker_id>', methods=['GET'])
@token_required
def get_one_tracker(current_user, tracker_id):
    tracker = Tracker.query.filter_by(
        id=tracker_id, user_id=current_user.id).first()

    if not tracker:
        return jsonify({'message': 'No todo found!'})

    tracker_data = {}
    tracker_data['id'] = tracker.id
    tracker_data['name'] = tracker.name
    tracker_data['desc'] = tracker.desc
    tracker_data['trackertype'] = tracker.trackertype
    tracker_data['lastused'] = tracker.lastused

    return jsonify(tracker_data)


@app.route('/updatelog/<tracker_id>/<log_id>', methods=['POST'])
@token_required
def update_log(current_user, tracker_id, log_id):
    log = Logs.query.filter_by(
        id=log_id, user_id=current_user.id, trackerid=tracker_id).first()

    if not log:
        return jsonify({'message': 'No log found!'})

    data = request.get_json()
    log.value = data["value"]
    log.note = data["note"]
    log.timestamp = datetime.strptime(
        data["timestamp"], "%a, %d %b %Y %H:%M:%S %Z")
    db.session.add(log)
    db.session.commit()
    return jsonify({'message': 'Log updated!'})


@app.route('/export/trackercsv', methods=['GET'])
@token_required
def download_datatracker(current_user):
    query_sets = Tracker.query.filter_by(user_id=current_user.id).all()
    column_names = ['name', "trackertype", 'desc']

    excel.init_excel(app)

    return excel.make_response_from_query_sets(query_sets, column_names, "csv", file_name="export.csv")


@app.route("/export/trackerpdf", methods=['GET'])
@token_required
def export_pdftracker(current_user):
    trackers = Tracker.query.filter_by(user_id=current_user.id).all()

    rendered = render_template("tracker_pdf_report.html", trackers=trackers, username=current_user.name,
                               useremail=current_user.email, downloadtime=datetime.now())
    pdf = pdfkit.from_string(
        rendered, False)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=report.pdf'

    return response


@app.route('/export/<tracker_id>/logcsv', methods=['GET'])
@token_required
def download_datalog(current_user, tracker_id):
    query_sets = Logs.query.filter_by(
        user_id=current_user.id, trackerid=tracker_id).all()
    tracker = Tracker.query.filter_by(
        user_id=current_user.id, id=tracker_id).first()
    column_names = ['trackerid', 'value', "note", 'timestamp']

    excel.init_excel(app)
    extension_type = "csv"
    filename = tracker.name + "_AllLogs" + "." + extension_type

    return excel.make_response_from_query_sets(query_sets, column_names, extension_type, file_name=filename)


@app.route("/export/<tracker_id>/logpdf", methods=['GET'])
@token_required
def export_pdflog(current_user, tracker_id):
    query_sets = Logs.query.filter_by(
        user_id=current_user.id, trackerid=tracker_id).all()

    tracker = Tracker.query.filter_by(
        user_id=current_user.id, id=tracker_id).first()

    rendered = render_template("pdf_report.html", logs=query_sets, username=current_user.name,
                               useremail=current_user.email, trackername=tracker.name, downloadtime=datetime.now())
    pdf = pdfkit.from_string(
        rendered, False)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=report.pdf'

    return response


@app.route('/google/auth', methods=['POST'])
def google_auth():

    auth = request.get_json()
    euser = User.query\
        .filter_by(email=auth.get('email'))\
        .first()
    if not euser:
        # database ORM object
        euser = User(

            name=auth.get("name"),
            email=auth.get('email'),
            public_id=str(uuid.uuid4()),

            joined=datetime.now(),
            lastvisit=datetime.now()

        )
        # insert user
        db.session.add(euser)
        db.session.commit()
        token = jwt.encode({
            'public_id': euser.public_id,
            'exp': datetime.utcnow() + timedelta(minutes=30)
        }, app.config['SECRET_KEY'])

        return make_response(jsonify({'token': token.decode('UTF-8')}), 201)
    token = jwt.encode({
        'public_id': euser.public_id,
        'exp': datetime.utcnow() + timedelta(minutes=30)
    }, app.config['SECRET_KEY'])

    return make_response(jsonify({'token': token.decode('UTF-8')}), 201)


@app.route('/<tracker_id>/plot', methods=['GET'])
@token_required
def gen_chart_url(current_user, tracker_id):
    logs = Logs.query.filter_by(
        user_id=current_user.id, trackerid=tracker_id).all()
    tracker = Tracker.query.filter_by(
        id=tracker_id, user_id=current_user.id).first()
    if (len(logs) == 0):
        return "nothing to show"
    yes = 0
    no = 0
    if (tracker.trackertype == "Boolean"):
        for log in logs:
            if log.value == "Yes":
                yes = yes + 1
            elif log.value == "No":
                no = no + 1
        img = BytesIO()
        labely = ['Yes', 'No']

        data = [yes, no]

        # Creating plot
        fig = plt.figure(figsize=(5, 2))
        plt.pie(data, labels=labely)
        plt.savefig(img, format='png')
        plt.close()
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode('utf8')

        return jsonify({'url': plot_url})
    if (tracker.trackertype == "Numerical"):
        data = []
        labelN = []
        
        for log in logs:
            
            data.append(log.value)
            labelN.append(str(log.timestamp.time())[0:5])
        img = BytesIO()
        new_dict = {labelN[i]: data[i] for i in range(len(data))}
        final = sorted(new_dict.items(), key=lambda x: x[1])

        sortdict = dict(final)

        plt.bar(sortdict.keys(), sortdict.values(), width=0.1)
        plt.xlabel('Log SNo.', fontsize=15)

        plt.ylabel('Values', fontsize=15)

        plt.savefig(img, format='png')
        plt.close()
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode('utf8')

        return jsonify({'url': plot_url})
    if (tracker.trackertype == "Time Duration"):
        data = []
        labelN = []
        
        for log in logs:
        
            data.append(log.value)
            labelN.append(str(log.timestamp.time())[0:5])
        img = BytesIO()
        new_dict = {labelN[i]: data[i] for i in range(len(data))}
        final = sorted(new_dict.items(), key=lambda x: x[1])

        sortdict = dict(final)

        plt.bar(sortdict.keys(), sortdict.values(), width=0.1)
        plt.xlabel('Log SNo.', fontsize=15)

        plt.ylabel('Values', fontsize=15)

        plt.savefig(img, format='png')
        plt.close()
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode('utf8')

        return jsonify({'url': plot_url})

# monthly progressreport


@celery.task(name='monthly_report')
def monthly_report():
    with app.app_context():

        users = User.query.filter_by().all()

        for user in users:
            logs = Logs.query.filter_by(
                user_id=user.id).all()
            trackers = Tracker.query.filter_by(user_id=user.id).all()

            rendered = render_template("monthly_progress.html", username=user.name,
                                       useremail=user.email, nooftracker=len(trackers), nooflog=len(logs), logs=logs, trackers=trackers, downloadtime=datetime.now(), month=datetime.now().month)
            pdf = pdfkit.from_string(
                rendered, False)

            msg3 = Message(
                user.name+", Your Monthly Progress Report -quansApp",
                sender='saurabhsatapathy0@gmail.com',
                recipients=[user.email],
            )
            msg3.html = render_template('mailhtmlreport.html', nooftracker=len(
                trackers), nooflog=len(logs), month=datetime.now().month)
            msg3.body = 'Hello, '+user.name + \
                '\nWe have noticed that you have not tracked anything in last 24 hours!! Track something Now.  '
            msg3.attach("Monthly_report", "application/pdf", pdf)
            mail.send(msg3)


if __name__ == "__main__":
    # setting debug to True enables hot reload
    # and also provides a debugger shell
    # if you hit an error while running the server
    app.run(debug=True)
