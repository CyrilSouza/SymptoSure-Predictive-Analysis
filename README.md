# SymptoSure Predictive Analysis

SymptoSure Predictive Analysis is a web application that predicts diseases based on user-input symptoms.

## Features

- User authentication (signup and login)
- Disease prediction based on symptoms
- Email notifications for disease prediction results
- SMS notifications for OTP verification during signup

## Prerequisites

Make sure you have the following installed:

- Python
- Flask
- Flask-PyMongo
- Flask-Mail
- Twilio
- NumPy
- scikit-learn

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/symptosure-predictive-analysis.git


2.Navigate to the project directory:
```
cd symptosure-predictive-analysis
```
3.Install dependencies:
```
pip install -r requirements.txt
```
## Usage
1.Run the Flask application:
```
python app7.py
```
Access the application in your web browser at http://localhost:5000.

## Configuration

Configure MongoDB URI in app7.py:

app.config['MONGO_URI'] = 'mongodb://localhost:27017/symptosure_predictive_analysis_db'
```
Configure Twilio account details in app7.py:
TWILIO_ACCOUNT_SID = 'your_account_sid'
TWILIO_AUTH_TOKEN = 'your_auth_token'
TWILIO_PHONE_NUMBER = 'your_twilio_phone_number'

Configure Flask-Mail in app7.py:
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_email_password'

```


## Contributing
Feel free to contribute to the development of this project. Pull requests are welcome.

## License
This project is licensed under the MIT License - see the LICENSE file for details.


Again, replace placeholders like `your-username`, `your_account_sid`, `your_auth_token`, `your_twilio_phone_number`, `your_email@gmail.com`, and `your_email_password` with your actual details.
