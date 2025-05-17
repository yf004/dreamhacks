from utils import *

from flask import Flask, redirect, url_for, session, render_template, request, jsonify
from authlib.integrations.flask_client import OAuth
import os
from config import *


app = Flask(__name__)
app.secret_key = CLIENT_SECRET

# OAuth Setup
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    access_token_url='https://oauth2.googleapis.com/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params={'access_type': 'offline', 'prompt': 'consent'},
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid email profile'},
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',

)

@app.route("/")
def home(): #bruhhhhhhhhhhhhhhhhh i was so confused pls oml
    return render_template("landing_page.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/signin")
def signin():
    return render_template("signin.html")

@app.route("/home_page")
def home_page():
    return render_template("home_page.html")

@app.route('/signup_w_google')
def signup_w_google():
    redirect_uri = url_for('auth_callback', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/auth/callback')
def auth_callback():
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()
    session['email'] = user_info['email']
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(use_reloader=True, debug=True) # for auto-reloading cos yay

    '''
    python app.py
    
    flask run --host=0.0.0.0 --port=8000 -> connect via wifi w another device
    flask run -> if nth works ig

    
    '''
