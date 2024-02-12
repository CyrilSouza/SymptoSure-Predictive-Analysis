import pickle
import numpy as np
from flask import Flask, request, render_template, redirect, url_for, session
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
from bson import ObjectId
import os
from twilio.rest import Client
import random

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/disease_predictor_db'
app.config['SECRET_KEY'] = os.urandom(24)

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'maxdsouza3031@gmail.com'  
app.config['MAIL_PASSWORD'] = 'pypcsloodzwtuijt'  

# Twilio configuration
TWILIO_ACCOUNT_SID = 'AC089ad7afe8d9f21496b83fbe59e68498'
TWILIO_AUTH_TOKEN = '3ec2bac3953559a7403802c07f20c677'
TWILIO_PHONE_NUMBER = '+18184958461'
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

mail = Mail(app)
mongo = PyMongo(app)

# Load the model
with open('svm_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Load the symptom index dictionary
with open('symptom_index.pkl', 'rb') as f:
    symptom_index = pickle.load(f)

# Load the predictions classes
with open('predictions_classes.pkl', 'rb') as f:
    predictions_classes = pickle.load(f)

def send_otp(phone_number, otp):
    try:
        message = client.messages.create(
            body=f'Your OTP for signup is: {otp}',
            from_=TWILIO_PHONE_NUMBER,
            to=phone_number
        )
        print("SMS sent successfully!")
        return message.sid
    except Exception as e:
        print(f"Failed to send SMS: {e}")
        return None

def send_prediction_report(email, prediction, symptoms):
    try:
        msg = Message('Disease Prediction Report', sender='maxdsouza3031@gmail.com', recipients=[email])
        
        
        email_content = render_template('email_template.html', prediction=prediction, symptoms=symptoms)
        print("Email Content:", email_content)  
        msg.html = email_content

        mail.send(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")


@app.route('/')
def login_page():
    error = session.pop('error', None)
    return render_template('login.html', error=error)

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user_data = mongo.db.users.find_one({'username': username})

        if user_data and check_password_hash(user_data['password'], password):
            session['user_id'] = str(user_data['_id'])
            return redirect(url_for('home'))
        else:
            session['error'] = 'Invalid credentials. Please try again or Signup as a new user'
            return render_template('login.html', error=session['error'])

    return redirect(url_for('login_page'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        phone_number = request.form['phone_number']

        # Generate OTP
        otp = ''.join(random.choices('0123456789', k=6))

        # Save user data to MongoDB
        existing_user = mongo.db.users.find_one({'$or': [{'username': username}, {'phone_number': phone_number}]})

        if existing_user:
            return render_template('login.html', error='Username or phone number already exists. Please log in.')

        user_data = {
            'username': username,
            'password': generate_password_hash(password, method='sha256'),
            'phone_number': phone_number,
            'otp': otp
        }

        result = mongo.db.users.insert_one(user_data)
        session['user_id'] = str(result.inserted_id)

        # Send OTP to the user's phone number
        send_otp(phone_number, otp)

        return render_template('verify_otp.html', message='OTP sent to your phone. Please verify.')

    return render_template('signup7.html')

@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    if request.method == 'POST':
        otp_attempt = request.form['otp_attempt']

        if 'user_id' in session:
            user_id = session['user_id']
            user_data = mongo.db.users.find_one({'_id': ObjectId(user_id)})
            saved_otp = user_data.get('otp', '')

            if otp_attempt == saved_otp:
                return redirect(url_for('home'))
            else:
                session['error'] = 'Invalid OTP. Please try again.'
                return render_template('verify_otp.html', error=session['error'])

    return redirect(url_for('login_page'))


@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))

    return render_template('index3.html')

@app.route('/predict', methods=['POST'])
def predict():
    symptom1 = request.form['symptom1']
    symptom2 = request.form['symptom2']
    symptom3 = request.form['symptom3']

    input_data = [0] * len(symptom_index)
    input_data[symptom_index[symptom1]] = 1
    input_data[symptom_index[symptom2]] = 1
    input_data[symptom_index[symptom3]] = 1
    input_data = np.array(input_data).reshape(1, -1)

    prediction = predictions_classes[model.predict(input_data)[0]]

    if 'user_id' in session:
        user_id = session['user_id']
        user_data = {
            'user_id': user_id,
            'symptoms': [symptom1, symptom2, symptom3],
            'prediction': prediction
        }
        mongo.db.user_searches.insert_one(user_data)

        user_email = mongo.db.users.find_one({'_id': ObjectId(user_id)})['username']
        symptoms_list = [symptom1, symptom2, symptom3]
        send_prediction_report(user_email, prediction, symptoms_list)

    return render_template('index3.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
