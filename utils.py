# empty for now :(

'''

deepseek api

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY
    )
    completion = client.chat.completions.create(
        extra_body={},
        model="deepseek/deepseek-r1:free",
        messages=[
            {
                "role": "user",
                "content": f"Rate this quip on a scale of 1-10: {user_input}, for the question: {question}, return a number from 1-10, inclusive, based on how funny, quirky and original the response was."
            }
        ]
    )
    ans = completion.choices[0].message.content




    

words

import nltk
from nltk.corpus import words
nltk.download('words', quiet=True)





firestore

app = Flask(__name__)
cred = credentials.Certificate("firebase-key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


# load allowed names
names_docs = db.collection("allowedNames").get()
allowedNames = []

for doc in names_docs:
    allowedNames = doc.to_dict().get('names')


import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.base_query import FieldFilter

cred = credentials.Certificate("firebase-key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

nameList = db.collection("allowedNames").document('allowedNames')
nameList.set({
    "names": lis
})

for name in lis:
    user_ref = db.collection("onlineUsers").document(name)
    user_ref.set({
        "username": name,
        "online": False,
        "lastSeen": firestore.SERVER_TIMESTAMP
    })

names_docs = db.collection("allowedNames").get()
names_list = []

for doc in names_docs:
    names_list = doc.to_dict().get('names')

print(names_list)
'''

