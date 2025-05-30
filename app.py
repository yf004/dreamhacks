
from flask import Flask, redirect, url_for, session, render_template, request, jsonify
from authlib.integrations.flask_client import OAuth
import os
from config import *
import firebase_admin
from firebase_admin import credentials, auth, firestore
from werkzeug.security import check_password_hash, generate_password_hash

from typing import List, Dict
from util.utils import *
from datetime import datetime



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
def index(): #bruhhhhhhhhhhhhhhhhh i was so confused pls oml
    return render_template("landing_page.html")

@app.route("/signup_page")
def signup_page():
    if 'is_logged_in' in session and session['is_logged_in']:
        return redirect('/home')
    return render_template("signup.html")

@app.route("/signin_page")
def signin_page():
    print('called3')
    if 'is_logged_in' in session and session['is_logged_in']:
        return redirect('/home')

    return render_template("signin.html")

@app.route('/signup_w_google')
def signup_w_google():
    print('called1')
    curr_url = url_for(request.args.get('curr_url'))
    session['curr_url'] = curr_url
    redirect_uri = url_for('auth_callback', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/auth/callback')
def auth_callback():
    print('called2')
    token = google.authorize_access_token()

    resp = google.get('userinfo')
    user_info = resp.json()

    session['email'] = user_info['email']
    session['is_logged_in'] = True
    
    curr_url = session['curr_url']
    session['curr_url'] = None

    return redirect(curr_url)

@app.route('/get_prompt', methods=['POST'])  
def get_prompt():
    prompt = get_journaling_prompt([])
    return jsonify({'prompt': prompt})

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form.get('username')
    password = request.form.get('password')

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

@app.route('/home')
def home():
    if 'is_logged_in' in session and session['is_logged_in']:
        return render_template("home.html")
    return redirect('/signin_page')

@app.route('/chat')
def chat():
    if 'is_logged_in' in session and session['is_logged_in']:
        context = retrieve_latest_entries()
        print(context)
        global chatbot
        chatbot = TherapyChatbot(context)

        return render_template('chat.html')
    return redirect('/signin_page')

@app.route('/journal')
def journal():
    if 'is_logged_in' in session and session['is_logged_in']:
        return render_template('journal.html')
    return redirect('/signin_page')

@app.route('/get_username', methods=['GET'])
def get_data():
    if 'email' in session:
        user = session['email']
        return jsonify({"name": user})
    elif 'username' in session:
        user = session['email']
        return jsonify({"name": user})
    else:
        redirect('/signin_page')

@app.route('/get_ai_analysis', methods=['POST'])
def get_ai_analysis():
    entry = request.form.get('entry')
    day = request.form.get('day')
    month = request.form.get('month')
    
    if 'email' in session:
        username = session['email']
    else:
        username = session['username']

    key = f"{day}-{month}"

    # if exists, return
    temp = retrieve_ai_response(username, day, month)
    if (temp != ''): return jsonify({'response': temp}), 200
    
    # else, generate and save
    ai_response = get_response_to_journal(entry)
    doc_ref = db.collection('usernames').document(username)
    doc = doc_ref.get()
    if not doc.exists:
        doc_ref.set({
            'journal_entries': {
                key: {
                    'ai_response': ai_response
                }
            }
        })
    else:
        doc_ref.set({
            'journal_entries': {
                key: {
                    'ai_response': ai_response
                }
            }
        }, merge=True)
    return jsonify({'response': ai_response}), 200

@app.route('/get_chatbot_response', methods=['POST'])
def get_chatbot_response():
    message = request.form.get('message')
    mode = request.form.get('mode')
    response = chatbot.chat(message, mode)
    print(message, mode)
    print(response)
    return jsonify({'response': response}), 200

@app.route('/get_chatbot_summary', methods=['GET'])
def get_chatbot_summary():
    response = chatbot.chatbot.summarize_session()
    save_chat(response)
    return jsonify({'response': response}), 200

@app.route('/new_chat', methods=['GET'])
def new_chat():
    context = retrieve_latest_entries
    global chatbot
    chatbot = TherapyChatbot(context)
    return jsonify({'response': 'done'}), 200

@app.route('/journal_entry', methods=['POST', 'GET'])  
def journal_entry():
    if 'email' in session:
        username = session['email']
    elif 'username' in session:
        username = session['username']
    else:
        return redirect('/signin_page')


    if request.method == 'POST':
        day = request.form.get('day')
        month = request.form.get('month')
    else:  # GET method
        day = request.args.get('day')
        month = request.args.get('month')

    print(username)
    print(day, month)
    entry = retrieve_entry(username, day, month)
    print('entry:', entry)
    return render_template("journal_entry.html", entry=str(entry), day=day, month=month)

@app.route('/get_journal_entry', methods=['POST'])  
def get_journal_entry():
    if 'email' in session:
        username = session['email']
    elif 'username' in session:
        username = session['username']
    else:
        return jsonify({'error': 'Not logged in'}), 401

    day = request.form.get('day')
    month = request.form.get('month')

    entry = retrieve_entry(username, day, month)
    print(day, month)
    print('entry:', entry)
    date = f"{day} {month}"
    return jsonify({'entry': entry, "date": date})

def retrieve_entry(username, day, month):

    try:
        doc_ref = db.collection('usernames').document(username)
        doc = doc_ref.get()

        if doc.exists:
            data = doc.to_dict()

            # Create a unique key like '10-May' for lookup
            entries = data.get('journal_entries', {})
            key = f"{day}-{month}"
            return entries.get(key, {}).get('entry', '')

    except Exception as e:
        print(f"Error retrieving entry: {e}")
        return '' 
    
    return ''  

def retrieve_ai_response(username, day, month):
    try:
        doc_ref = db.collection('usernames').document(username)
        doc = doc_ref.get()

        

        if doc.exists:
            data = doc.to_dict()

            # Create a unique key like '10-May' for lookup
            entries = data.get('journal_entries', {})
            key = f"{day}-{month}"
            return entries.get(key, {}).get('ai_response', '')

    except Exception as e:
        print(f"Error retrieving entry: {e}")
        return '' 
    
    return ''  

def retrieve_latest_entries():
    try:
        if 'email' in session:
            username = session['email']
        elif 'username' in session:
            username = session['username']
        else:
            return []
        doc_ref = db.collection('usernames').document(username)
        doc = doc_ref.get()

        if doc.exists:
            data = doc.to_dict()
            entries = data.get('journal_entries', {})

            # Convert keys like '10-May' into datetime objects for sorting
            def parse_date(key):
                try:
                    return datetime.strptime(key, "%d-%B")  # e.g., "10-May"
                except ValueError:
                    return datetime.min  # Handle unexpected format safely

            # Sort keys by date, newest first
            sorted_keys = sorted(entries.keys(), key=parse_date, reverse=True)

            latest_entries = []
            for key in sorted_keys[:10]: 
                entry = entries.get(key, {}).get('summary', '')
                if entry:
                    latest_entries.append(entry)

            return latest_entries

    except Exception as e:
        print(f"Error retrieving latest entries: {e}")
        return []

    return []

@app.route('/retrieve_mood', methods=['POST']) 
def retrieve_mood():
    try:
        

        if 'email' in session:
            username = session['email']
        elif 'username' in session:
            username = session['username']
        else:
            return jsonify({'error': 'Not Logged In'}), 200
        
        doc_ref = db.collection('usernames').document(username)
        doc = doc_ref.get()


        day = request.form.get('day')
        month = request.form.get('month')

        if doc.exists:
            data = doc.to_dict()

            # Create a unique key like '10-May' for lookup
            entries = data.get('journal_entries', {})
            key = f"{day}-{month}"
            mood = entries.get(key, {}).get('mood', '')
            return jsonify({'mood': mood}), 200

    except Exception as e:
        print(f"Error retrieving entry: {e}")
        return jsonify({'error': e}), 200

@app.route('/save_entry', methods=['POST']) 
def save_entry():
    """Save a journal entry for a specific user, day, and month."""
    try:
        day = request.form.get('day')
        month = request.form.get('month')
        entry = request.form.get('entry')

        summary = get_journal_summary(entry)
        if 'email' in session:
            username = session['email']
        else:
            username = session['username']

        key = f"{day}-{month}"

        doc_ref = db.collection('usernames').document(username)
        doc = doc_ref.get()
        if not doc.exists:
            doc_ref.set({
                'journal_entries': {
                    key: {
                        'entry': entry,
                        'summary': summary
                    }
                }
            })
        else:
            doc_ref.set({
                'journal_entries': {
                    key: {
                        'entry': entry,
                        'summary': summary
                    }
                }
            }, merge=True)

    except Exception as e:
        print(f"Error saving entry: {e}")
    return jsonify({'message': 'Entry saved successfully'}), 200

@app.route('/save_chat', methods=['GET'])
def save_chat(summary:str):
    """Save a journal entry for a specific user, day, and month."""
    try:
        summary = chatbot.summarize_session()
        if 'email' in session:
            username = session['email']
        elif 'username' in session:
            username = session['username']
        else: return

        doc_ref = db.collection('usernames').document(username)
        doc = doc_ref.get()

        chat = chatbot.save_entire_history()
        id = chat.get('id')
        time = chat.get('time')
        history = chat.get('history')
        if not doc.exists:
            doc_ref.set({
                'chats': {
                    time: {
                        'id': id,
                        'history': history,
                        'summary': summary
                    }
                }
            })
        else:
            doc_ref.set({
                'chats': {
                    time: {
                        'id': id,
                        'history': history,
                        'summary': summary
                    }
                }
            }, merge=True)

        

    except Exception as e:
        print(f"Error saving entry: {e}")
    chatbot = TherapyChatbot()
    return jsonify({'summary': summary}), 200

@app.route('/save_mood', methods=['POST']) 
def save_mood():
    """Save a journal entry for a specific user, day, and month."""
    try:
        mood = request.form.get('mood')
        day = request.form.get('day')
        month = request.form.get('month')

        if 'email' in session:
            username = session['email']
        else:
            username = session['username']

        key = f"{day}-{month}"

        doc_ref = db.collection('usernames').document(username)
        doc = doc_ref.get()
        if not doc.exists:
            doc_ref.set({
                'journal_entries': {
                    key: {
                        'mood': mood,
                    }
                }
            })
        else:
            doc_ref.set({
                'journal_entries': {
                    key: {
                        'mood': mood,
                    }
                }
            }, merge=True)

    except Exception as e:
        print(f"Error saving entry: {e}")
    return jsonify({'message': 'Entry saved successfully'}), 200

if __name__ == "__main__":
    app.run(use_reloader=True, debug=True) # for auto-reloading cos yay

    '''
    python app.py
    
    flask run --host=0.0.0.0 --port=8000 -> connect via wifi w another device
    flask run -> if nth works ig

    
    '''
