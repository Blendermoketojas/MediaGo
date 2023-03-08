from flask import Flask, request, jsonify
from pymongo import MongoClient

MANGO_URI = "mongodb+srv://admin:admin123@cluster0.l4umf8e.mongodb.net/?retryWrites=true&w=majority"

app = Flask(__name__)
cluster = MongoClient(MANGO_URI)
db = cluster['users']
users = db['users']

@app.route('/register', methods=['POST'])
def process_register():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        if json.get('user') and json.get('email') and json.get('password'):
            result = users.insert_one(json)
            return f"Created user with ID {result.inserted_id}"
        else:
            return 'Bad json keys'
    else:
        return 'Content-Type not supported!'

@app.route('/login', methods=['POST'])
def process_login():
    content_type == request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        if json.get('user') and json.get('password'):
            #Login metodas is mongoDB
            return
        else:
            return 'Bad json keys'
    else:
        return 'Content-Type not supported!'

if __name__ == "__main__":
    app.run()
