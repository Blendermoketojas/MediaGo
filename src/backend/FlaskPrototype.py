from flask import Flask, request, jsonify
import mysql.connector
from passlib.hash import bcrypt_sha256
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "plugdj"
)

cursor = mydb.cursor()

preset = "$bcrypt-sha256$v=2,t=2b,r=12$"
salt = "plugdj13"

def registration(nickname, email, password):
    sql = "SELECT EXISTS(SELECT id_users FROM users WHERE nickname = %s)"
    val = (nickname,)
    cursor.execute(sql, val)
    if (cursor.fetchall()[0][0] != 0):
        return jsonify({'success':False, 'message':'nickname'})
    sql = "SELECT EXISTS(SELECT id_users FROM users WHERE email = %s)"
    val = (email,)
    cursor.execute(sql, val)
    if (cursor.fetchall()[0][0] != 0):
        return jsonify({'success':False, 'message':'email'})
    
    temp = nickname+email
    id = bcrypt_sha256.hash(temp)[len(preset):]
    password = bcrypt_sha256.hash(salt+password)[len(preset):]

    sql = "INSERT INTO users (id_users, nickname, email, password) VALUES (%s, %s, %s, %s)"
    val = (id, nickname, email, password)
    cursor.execute(sql, val)
    mydb.commit()

    return jsonify({'success':True, 'id':id, 'nickname':nickname})

def login(email, password):
    sql = "SELECT EXISTS(SELECT id_users FROM users WHERE email = %s)"
    val = (email,)
    cursor.execute(sql, val)
    response = cursor.fetchall()[0][0]
    if(response == 0):
        return jsonify({'success':False, 'message':'email'})
    
    sql = "SELECT * FROM users WHERE email = %s"
    val = (email,)
    cursor.execute(sql, val)
    response = cursor.fetchall()
    id = "null"
    hashpassword = "null"
    for row in response:
        id = row[3]
        hashpassword = row[2]
    
    print(response)

    if(bcrypt_sha256.verify(salt+password, preset+hashpassword) == True):
        sql = "SELECT nickname FROM users WHERE id_users = %s"
        val = (id,)
        cursor.execute(sql, val)
        nickname = cursor.fetchall()[0][0]
        return jsonify({'success':True, 'id':id, 'nickname':nickname})
    else:
        return jsonify({'success':False, 'message':'password'})


@app.route('/register', methods=['POST'])
def process_r():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        if json.get('nickname') and json.get('email') and json.get('password'):         
            
            return registration(json.get('nickname'), json.get('email'), json.get('password'))
        else:
            return jsonify({'success':False, 'message':'JSON keys not supported!'})
    else:
        return jsonify({'success':False, 'message':'Content type not supported!'})

@app.route('/login', methods=['POST'])
def process_l():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        if json.get('email') and json.get('password'):

            return login(json.get('email'), json.get('password'))
        else:
            return jsonify({'success':False, 'message':'JSON keys not supported!'})
    else:
        return jsonify({'success':False, 'message':'Content type not supported'})

if __name__ == "__main__":
    app.run()


# @app.route('/update_playlist_add')
# def process_addition_playlist():
#     content_type = request.headers.get('Content-Type')
#     if (content_type == 'application/json'):
#         json = request.json
#         if json.get('username') and json.get('token') and json.get('song'):
#             #Muzikos pridejimo metodas i mongodb
#             #if result.acknowledged == False:
#                 #return jsonify({'success':False, 'message':'reason TBA'})
#             return
#         else:
#             return jsonify({'success':False, 'message':'JSON keys not supported!'})
#     else:
#         return jsonify({'success':False, 'message':'Content type not supported'})
    

# @app.route('/update_playlist_move')
# def process_move_playlist():
#     content_type = request.headers.get('Content-Type')
#     if (content_type == 'application/json'):
#         json = request.json
#         if json.get('username') and json.get('token'):
#             #Muzikos perkelimo metodas mongodb
#             #if result.acknowledged == False:
#                 #return jsonify({'success':False, 'message':'reason TBA'})
#             return
#         else:
#             return jsonify({'success':False, 'message':'JSON keys not supported!'})
#     else:
#         return jsonify({'success':False, 'message':'Content type not supported'})
    

# @app.route('/update_playlist_remove')
# def process_move_playlist():
#     content_type = request.headers.get('Content-Type')
#     if (content_type == 'application/json'):
#         json = request.json
#         if json.get('username') and json.get('token') and json.get('song'):
#             #Muzikos salinimo metodas mongodb
#             #if result.acknowledged == False:
#                 #return jsonify({'success':False, 'message':'reason TBA'})
#             return
#         else:
#             return jsonify({'success':False, 'message':'JSON keys not supported!'})
#     else:
#         return jsonify({'success':False, 'message':'Content type not supported'})
    

# @app.route('/update_songs_add')
# def process_addition_songs():
#     content_type = request.headers.get('Content-Type')
#     if (content_type == 'application/json'):
#         json = request.json
#         if json.get('username') and json.get('token') and json.get('song'):
#             #Muzikos pridejimo metodas metodas mongodb
#             #if result.acknowledged == False:
#                 #return jsonify({'success':False, 'message':'reason TBA'})
#             return
#         else:
#             return jsonify({'success':False, 'message':'JSON keys not supported!'})
#     else:
#         return jsonify({'success':False, 'message':'Content type not supported'})
    
# #Tikriausiai nereikes
# @app.route('/update_songs_remove')
# def process_remove_songs():
#     content_type = request.headers.get('Content-Type')
#     if (content_type == 'application/json'):
#         json = request.json
#         if json.get('username') and json.get('token') and json.get('song'):
#             #Muzikos salinimo metodas mongodb
#             #if result.acknowledged == False:
#                 #return jsonify({'success':False, 'message':'reason TBA'})
#             return
#         else:
#             return jsonify({'success':False, 'message':'JSON keys not supported!'})
#     else:
#         return jsonify({'success':False, 'message':'Content type not supported'})
    

# @app.route('/update_server_add')
# def process_addition_server():
#     content_type = request.headers.get('Content-Type')
#     if (content_type == 'application/json'):
#         json = request.json
#         if json.get('username') and json.get('token') and json.get('server'):
#             #Muzikos salinimo metodas mongodb
#             #if result.acknowledged == False:
#                 #return jsonify({'success':False, 'message':'reason TBA'})
#             return
#         else:
#             return jsonify({'success':False, 'message':'JSON keys not supported!'})
#     else:
#         return jsonify({'success':False, 'message':'Content type not supported'})
    


