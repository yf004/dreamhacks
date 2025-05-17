
git clone https://github.com/yf004/dreamhacks.git
cd flask_project


python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate

pip install -r requirements.txt


TODO: config.py idk

python app.py

export FLASK_APP=app.py
export FLASK_ENV=development
flask run


