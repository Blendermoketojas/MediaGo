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

#########################################################################
#USER METHODS
#########################################################################

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
    
#########################################################################
#ROOM METHODS[CRUD] ()
#########################################################################

def server_add(name, description, owner, theme, genre, country):
    sql = "SELECT EXISTS(SELECT id_servers FROM servers WHERE name = %s)"
    val = (name,)
    cursor.execute(sql, val)
    if(cursor.fetchall()[0][0] != 0):
        return jsonify({'success':False, 'message':'name'})

    sql = "INSERT INTO servers (name, description, fk_themeid_theme, fk_countryid_country, fk_genreid_genre fk_usersid_users) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (name, description, theme, country, genre, owner)
    cursor.execute(sql, val)
    mydb.commit()

    sql = "SELECT id_servers FROM servers WHERE name = %s"
    val = (name,)
    cursor.execute(sql, val)

    id = cursor.fetchall()[0][0]

    return jsonify({'success':True, 'id':id, 'name':name, 'description':description, 'owner':owner, 'theme':theme, 'genre':genre, 'country':country})


def server_delete(id, user_id):
    sql = "SELECT * FROM servers WHERE id_server = %s"
    val = (id,)
    cursor.execute(sql, val)
    result = cursor.fetchall()
    if (result[0][0] != 0):
        for row in result:
            if(user_id == row[5]):
                sql = "DELETE FROM servers_users WHERE fk_serversid_servers = %s"
                val = (id,)
                cursor.execute(sql, val)
                mydb.commit()
                sql = "DELETE FROM servers WHERE id_server = %s"
                val = (id,)
                cursor.execute(sql, val)
                mydb.commit()
                return jsonify({'success':True, 'message':'Server with id: '+id+' , was deleted successfully'})
            else:
                return jsonify({'success':False, 'message':'user_id'})
    else:
        return jsonify({'success':False, 'message':'id'})

def server_edit_info(id, name, description, owner, theme, genre, country):
    sql = "SELECT * FROM servers WHERE id_servers = %s"
    val = (id,)
    cursor.execute(sql, val)
    response = cursor.fetchall()
    if(response[0][0] == 0):
        return jsonify({'success':False, 'message':'id'})
    else:
        for row in response:
            if(row[7] == owner):
                sql = "UPDATE servers SET name = %s, description = %s, fk_themeid_theme = %s, fk_countryid_country = %s, fk_genreid_genre = %s WHERE id_servers = %s"
                val = (name, description, theme, country, genre, id)
                cursor.execute(sql, val)
                mydb.commit()
                return jsonify({'success':True, 'id':id, 'description':description, 'name':name, 'owner':owner, 'theme':theme, 'genre':genre, 'country':country})
            else:
                return jsonify({'success':False, 'message':'user_id'})
            
def server_edit_owner(id, owner, newOwner):
    sql = "SELECT * FROM servers WHERE id_servers = %s"
    val = (id,)
    cursor.execute(sql, val)
    respone = cursor.fetchall()
    if(respone[0][0] == 0):
        return jsonify({'success':False, 'message':'id'})
    else:
        for row in respone:
            if(row[7] == owner):
                sql = "UPDATE servers SET fk_usersid_users = %s WHERE id_servers = %s"
                val = (newOwner, id)
                cursor.execute(sql, val)
                mydb.commit()

                sql = "SELECT * FROM servers WHERE id_servers = %s"
                val = (id,)
                cursor.execute(sql, val)
                respone = cursor.fetchall()
                for row in respone:
                    return jsonify({'success':True, 'id':row[3], 'name':row[0], 'description':row[1], 'users':row[2], 'owner':row[4], 'theme':row[5], 'genre':row[7], 'country':row[6]})
            else:
                return jsonify({'success':False, 'message':'user_id'})
#########################################################################
#DROPDOWN VALUES
#########################################################################

def get_countries():
    sql = "SELECT * FROM country"
    cursor.execute(sql)
    response = cursor.fetchall()
    data = {'success':True, 'data':{}}
    json = data['data']
    tempint = 0
    for row in response:
        json[tempint] = {}
        tempjson = json[tempint]
        tempjson['id'] = row[1]
        tempjson['name'] = row[0]
        tempint += 1

    return jsonify(data)

def get_genres():
    sql = "SELECT * FROM genre"
    cursor.execute(sql)
    response = cursor.fetchall()
    data = {'success':True, 'data':{}}
    json = data['data']
    tempint = 0
    for row in response:
        json[tempint] = {}
        tempjson = json[tempint]
        tempjson['id'] = row[1]
        tempjson['name'] = row[0]
        tempint += 1

    return jsonify(data)

def get_countries_e():
    #SELECT tb1.* FROM tb1 LEFT JOIN tb2 ON tb1.id = tb2.fk_id WHERE tb2.fk_id IS NULL
    sql = "SELECT * FROM country LEFT JOIN servers ON country.id_country = servers.fk_countryid_country WHERE servers.fk_countryid_country IS NOT NULL"
    cursor.execute(sql)
    response = cursor.fetchall()
    data = {'success':True, 'data':{}}
    json = data['data']
    try:
        tempint = 0
        for row in response:
            json[tempint] = {}
            tempjson = json[tempint]
            tempjson['id'] = row[1]
            tempjson['name'] = row[0]
            tempint += 1

        return jsonify(data)
    except:
        return jsonify({'success':False, 'message':'null'})

def get_genres_e():
    sql = "SELECT * FROM genre LEFT JOIN servers ON genre.id_genre = servers.fk_genreid_genre WHERE servers.fk_genreid_genre IS NOT NULL"
    cursor.execute(sql)
    response = cursor.fetchall()
    data = {'success':True, 'data':{}}
    json = data['data']
    try:
        tempint = 0
        for row in response:
            json[tempint] = {}
            tempjson = json[tempint]
            tempjson['id'] = row[1]
            tempjson['name'] = row[0]
            tempint += 1

        return jsonify(data)
    except:
        return jsonify({'success':False, 'message':'null'})
    return

#########################################################################
#ROOM GET DATA
#########################################################################

def get_server_info(id):
    sql = "SELECT * FROM servers WHERE id_servers = %s"
    val = (id,)
    cursor.execute(sql, val)
    response = cursor.fetchall()
    try:
        for row in response:
            return jsonify({'success':True, 'id':row[3], 'name':row[0], 'description':row[1], 'users':row[2], 'owner':row[4], 'theme':row[5], 'genre':row[7], 'country':row[6]})
    except:
        return jsonify({'success':False, 'message':'id'})
    
def get_servers(popular, genre, country, offset, limit):
    if limit > 50:
        limit = 50
    
    sql = "SELECT * FROM servers WHERE genre = %s AND country = %s ORDER BY users "
    if popular == True:
        sql += "ASC"
    else:
        sql += "DESC"

    sql += " LIMIT %s, %s;"
    val = (genre, country, offset, limit)
    cursor.execute(sql, val)
    response = cursor.fetchall()
    data = {'success':True, 'data':{}}
    json = data['data']
    try:
        tempint = 0
        for row in response:
            json[tempint] = {}
            tempjson = json[tempint]
            tempjson['id'] = row[3]
            tempjson['name'] = row[0]
            tempjson['genre'] = row[7]
            tempjson['country'] = row[6]
            tempjson['users'] = row[2]
            tempint += 1

        return jsonify(data)
    except:
        return jsonify({'success':False, 'message':'null'})

def get_servers(popular, country, offset, limit):
    if limit > 50:
        limit = 50
    
    sql = "SELECT * FROM servers WHERE country = %s ORDER BY users "
    if popular == True:
        sql += "ASC"
    else:
        sql += "DESC"

    sql += " LIMIT %s, %s;"
    val = (country, offset, limit)
    cursor.execute(sql, val)
    response = cursor.fetchall()
    data = {'success':True, 'data':{}}
    json = data['data']
    try:
        tempint = 0
        for row in response:
            json[tempint] = {}
            tempjson = json[tempint]
            tempjson['id'] = row[3]
            tempjson['name'] = row[0]
            tempjson['genre'] = row[7]
            tempjson['country'] = row[6]
            tempjson['users'] = row[2]
            tempint += 1

        return jsonify(data)
    except:
        return jsonify({'success':False, 'message':'null'})

def get_servers(popular, genre, offset, limit, temp, temp1):
    if limit > 50:
        limit = 50
    
    sql = "SELECT * FROM servers WHERE genre = %s ORDER BY users "
    if popular == True:
        sql += "ASC"
    else:
        sql += "DESC"

    sql += " LIMIT %s, %s;"
    val = (genre, offset, limit)
    cursor.execute(sql, val)
    response = cursor.fetchall()
    data = {'success':True, 'data':{}}
    json = data['data']
    try:
        tempint = 0
        for row in response:
            json[tempint] = {}
            tempjson = json[tempint]
            tempjson['id'] = row[3]
            tempjson['name'] = row[0]
            tempjson['genre'] = row[7]
            tempjson['country'] = row[6]
            tempjson['users'] = row[2]
            tempint += 1

        return jsonify(data)
    except:
        return jsonify({'success':False, 'message':'null'})

def get_servers(popular, offset, limit):
    if limit > 50:
        limit = 50
    
    sql = "SELECT * FROM servers ORDER BY users "
    if popular == True:
        sql += "ASC"
    else:
        sql += "DESC"

    sql += " LIMIT %s, %s;"
    val = (offset, limit)
    cursor.execute(sql, val)
    response = cursor.fetchall()
    print(response)
    data = {'success':True, 'data':{}}
    json = data['data']
    try:
        tempint = 0
        for row in response:
            json[tempint] = {}
            tempjson = json[tempint]
            tempjson['id'] = row[3]
            tempjson['name'] = row[0]
            tempjson['genre'] = row[7]
            tempjson['country'] = row[6]
            tempjson['users'] = row[2]
            tempint += 1

        print(data)
        return jsonify(data)
    except:
        return jsonify({'success':False, 'message':'null'})

#########################################################################
#USER METHODS (ROUTES)
#########################################################################

@app.route('/register', methods=['POST'])
def process_r():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        if json.get('nickname') and json.get('email') and json.get('password') and len(json) == 3:         
            
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
        if json.get('email') and json.get('password') and len(json) == 2:

            return login(json.get('email'), json.get('password'))
        else:
            return jsonify({'success':False, 'message':'JSON keys not supported!'})
    else:
        return jsonify({'success':False, 'message':'Content type not supported'})

#########################################################################
#ROOM METHODS[CRUD] (ROUTES)
#########################################################################

@app.route('/server_add', methods=['POST'])
def process_s_add():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        if json.get('name') and json.get('owner') and json.get('description') and isinstance(json.get('theme'), int) and isinstance(json.get('genre'), int) and isinstance(json.get('country'), int) and len(json) == 6:

            return server_add(json.get('name'), json.get('owner'), json.get('description'), json.get('theme'), json.get('genre'), json.get('country'))
        else:
            return jsonify({'success':False, 'message':'JSON keys not supported!'})
    else:
        return jsonify({'success':False, 'message':'Content type not supported'})
    

@app.route('/server_delete', methods=['POST'])
def process_s_delete():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        if isinstance(json.get('id'), int) and json.get('user_id') and len(json) == 2:

            return server_delete(json.get('id'), json.get('user_id'))
        else:
            return jsonify({'success':False, 'message':'JSON keys not supported!'})
    else:
        return jsonify({'success':False, 'message':'Content type not supported'})
    

@app.route('/server_edit_info', methods=['POST'])
def process_s_edit_i():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        if isinstance(json.get('id'), int) and json.get('name') and json.get('description') and json.get('user_id') and isinstance(json.get('theme'), int) and isinstance(json.get('genre'), int) and isinstance(json.get('country'), int) and len(json) == 7:

            return server_edit_info(json.get('id'), json.get('name'), json.get('description'), json.get('user_id'), json.get('theme'), json.get('genre'), json.get('country'))
        else:
            return jsonify({'success':False, 'message':'JSON keys not supported!'})
    else:
        return jsonify({'success':False, 'message':'Content type not supported'})
    
    
@app.route('/server_edit_owner', methods=['POST'])
def process_s_edit_o():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        if isinstance(json.get('id'), int) and json.get('user_id') and json.get('new_owner') and len(json) == 3:

            return server_edit_owner(json.get('id'), json.get('user_id'), json.get('new_owner'))
        else:
            return jsonify({'success':False, 'message':'JSON keys not supported!'})
    else:
        return jsonify({'success':False, 'message':'Content type not supported'})

#########################################################################
#DROPDOWN VALUES (ROUTES)
#########################################################################

@app.route('/get_dropdown_search', methods=['GET'])
def process_get_d_search():
    requestType = request.args.get('type', type = str)
    if requestType == "country":
        return get_countries_e()
    elif requestType == "genre":
        return get_genres_e()
    else:
        return jsonify({'success':False, 'message':'Argument not supported'})
    
@app.route('/get_dropdown_create', methods=['GET'])
def process_get_d_create():
    requestType = request.args.get('type', type = str)
    if requestType == "country":
        return get_countries()
    elif requestType == "genre":
        return get_genres()
    else:
        return jsonify({'success':False, 'message':'Argument not supported'})

#########################################################################
#ROOM GET DATA (ROUTES)
#########################################################################

@app.route('/get_server_info', methods=['POST'])
def process_s_info():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        if isinstance(json.get('id'), int) and len(json) == 1:

            return get_server_info(json.get('id'))
        else:
            return jsonify({'success':False, 'message':'JSON keys not supported!'})
    else:
        return jsonify({'success':False, 'message':'Content type not supported'})

@app.route('/get_servers', methods=['POST'])
def process_servers():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        if isinstance(json.get('popular'), bool) and isinstance(json.get('offset'), int) and isinstance(json.get('limit'), int) and len(json) == 3:
            
            return get_servers(json.get('popular'), json.get('offset'), json.get('limit'))

        if isinstance(json.get('popular'), bool) and isinstance(json.get('genre'), int) and isinstance(json.get('country'), int) and isinstance(json.get('offset'), int) and isinstance(json.get('limit'), int) and len(json) == 5:
            
            return get_server_info(json.get('popular'), json.get('genre'), json.get('country'), json.get('offset'), json.get('limit'))

        if isinstance(json.get('popular'), bool) and isinstance(json.get('genre'), int) and isinstance(json.get('offset'), int) and isinstance(json.get('limit'), int) and len(json) == 4:
            
            return get_servers(json.get('popular'), json.get('genre'), json.get('offset'), json.get('limit'))

        if isinstance(json.get('popular'), bool) and isinstance(json.get('country'), int) and isinstance(json.get('offset'), int) and isinstance(json.get('limit'), int) and len(json) == 4:
            
            return get_servers(json.get('popular'), json.get('country'), json.get('offset'), json.get('limit'), 'tt', 'tt')

        return jsonify({'success':False, 'message':'JSON keys not supported!'})
    else:
        return jsonify({'success':False, 'message':'Content type not supported'})


if __name__ == "__main__":
    app.run()