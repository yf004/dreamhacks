
from flask import Flask, redirect, url_for, session, render_template, request, jsonify
from authlib.integrations.flask_client import OAuth
import os
from config import *
import firebase_admin
from firebase_admin import credentials, auth, firestore
from werkzeug.security import check_password_hash, generate_password_hash

from typing import List, Dict
from util.utils import *



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

# Initialize Firebase Admin SDK
cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route("/")
def home(): #bruhhhhhhhhhhhhhhhhh i was so confused pls oml
    return render_template("landing_page.html")

@app.route("/signup_page")
def signup_page():
    if 'is_logged_in' in session and session['is_logged_in']:
        return redirect('/home_page')
    return render_template("signup.html")

@app.route("/signin_page")
def signin_page():
    if 'is_logged_in' in session and session['is_logged_in']:
        return redirect('/home_page')

    return render_template("signin.html")

@app.route("/home_page")
def home_page():
    if 'is_logged_in' in session and session['is_logged_in']:
        return render_template("home_page.html")
    return redirect('/')


    

@app.route('/signup_w_google', methods=['POST'])
def signup_w_google():
    curr_url = request.form.get('curr_url')
    session['curr_url'] = curr_url
    redirect_uri = url_for('auth_callback', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/auth/callback')
def auth_callback():
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()
    session['email'] = user_info['email']
    session['is_logged_in'] = True

    return redirect(session['curr_url'])

@app.route('/journal')  
def journal():
    return render_template("journal.html")

@app.route('/get_prompt', methods=['POST'])  
def get_prompt():
    prompt = get_journaling_prompt([])
    return jsonify({'prompt': prompt})


@app.route('/signup', methods=['POST'])
def signup():
    username = request.form.get('username')
    password = request.form.get('password ')

    username_ref = db.collection('usernames').document(username)

    try:
        user = auth.create_user(uid=username, password=password)


        password_hash = generate_password_hash(password)

        username_ref.set({
            'uid': user.uid,
            'username': username,
            'password_hash': password_hash
        })

        session['is_logged_in'] = True
        session['username'] = username

        return jsonify({'message': 'User created successfully', 'uid': user.uid}), 201

    except Exception as e:
        print(f"Error creating user: {e}")
        return jsonify({'error': str(e)}), 400
    

@app.route('/signin', methods=['POST'])
def signin():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400

    username_ref = db.collection('usernames').document(username)
    user_doc = username_ref.get()

    if not user_doc.exists:
        return jsonify({'error': 'User does not exist'}), 404

    user_data = user_doc.to_dict()
    stored_hash = user_data.get('password_hash')

    if stored_hash and check_password_hash(stored_hash, password):
        session['is_logged_in'] = True
        session['username'] = username
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401


@app.route('/user_exists', methods=['POST'])
def user_exists():
    username = request.form.get('username')


    username_ref = db.collection('usernames').document(username)

    if username_ref.get().exists:
        return jsonify({'error': 'Username already taken'}), 400
    else:
        return jsonify({'message': 'Username available'}), 200


@app.route('/logout')
def logout():
    session['is_logged_in'] = False
    if 'username' in session:
        session.pop('username', None)  
    if 'email' in session:
        session.pop('email', None)
    return redirect('/')


if __name__ == "__main__":
    app.run(use_reloader=True, debug=True) # for auto-reloading cos yay

    '''
    python app.py
    
    flask run --host=0.0.0.0 --port=8000 -> connect via wifi w another device
    flask run -> if nth works ig

    
    '''
