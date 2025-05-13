from flask import Flask, render_template, request, jsonify
from utils import *


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(use_reloader=True, debug=True) # for auto-reloading cos yay

    '''
    python app.py
    
    flask run --host=0.0.0.0 --port=8000 -> connect via wifi w another device
    flask run -> if nth works ig

    
    '''
