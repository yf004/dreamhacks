from flask import Flask, render_template, request, jsonify
from utils import *


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/main")
def main():
    return render_template("landing_page.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/signin")
def signin():
    return render_template("signin.html")




if __name__ == "__main__":
    app.run(use_reloader=True, debug=True) # for auto-reloading cos yay

    '''
    python app.py
    
    flask run --host=0.0.0.0 --port=8000 -> connect via wifi w another device
    flask run -> if nth works ig

    
    '''
