from flask import Flask

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Set your secret key for sessions
app.config['SESSION_COOKIE_NAME'] = "Ishmam's Cookie"
app.config["CORS_HEADERS"] = 'Content-Type'

