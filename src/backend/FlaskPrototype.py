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
    password = "root",
    database = "plugdj"
)

cursor = mydb.cursor()

preset = "$bcrypt-sha256$v=2,t=2b,r=12$"
salt = "plugdj13"

#SOME STUFF

is_busy = False

def wait_check():
    global is_busy
    while is_busy == True:
        if is_busy == False:
            return
    return

db_country = {}
db_genre = {}

def getCountryGenre():
    global db_genre
    global db_country
    
    sql = "SELECT * FROM genre"
    cursor.execute(sql)
    response = cursor.fetchall()

    for row in response:
        db_genre[row[1]] = row[0]

    sql = "SELECT * FROM country"
    cursor.execute(sql)
    response = cursor.fetchall()

    for row in response:
        db_country[row[1]] = row[0]

#########################################################################
#USER METHODS
#########################################################################

def registration(nickname, email, password):
    wait_check()
    global is_busy
    is_busy = True
    
    sql = "SELECT EXISTS(SELECT id_users FROM users WHERE nickname = %s)"
    val = (nickname,)
    cursor.execute(sql, val)
    if (cursor.fetchall()[0][0] != 0):
        is_busy = False
        
        return jsonify({'success':False, 'message':'nickname'})
    sql = "SELECT EXISTS(SELECT id_users FROM users WHERE email = %s)"
    val = (email,)
    cursor.execute(sql, val)
    if (cursor.fetchall()[0][0] != 0):
        is_busy = False
        
        return jsonify({'success':False, 'message':'email'})
    
    temp = nickname+email
    id = bcrypt_sha256.hash(temp)[len(preset):]
    password = bcrypt_sha256.hash(salt+password)[len(preset):]

    sql = "INSERT INTO users (id_users, nickname, email, password) VALUES (%s, %s, %s, %s)"
    val = (id, nickname, email, password)
    cursor.execute(sql, val)
    mydb.commit()

    is_busy = False
        
    return jsonify({'success':True, 'id':id, 'nickname':nickname})

def login(email, password):
    wait_check()
    global is_busy
    is_busy = True

    sql = "SELECT EXISTS(SELECT id_users FROM users WHERE email = %s)"
    val = (email,)
    cursor.execute(sql, val)
    response = cursor.fetchall()[0][0]
    if(response == 0):
        is_busy = False
        
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
        is_busy = False
        
        return jsonify({'success':True, 'id':id, 'nickname':nickname})
    else:
        is_busy = False
        
        return jsonify({'success':False, 'message':'password'})
    
#########################################################################
#ROOM METHODS[CRUD] ()
#########################################################################

def server_add(name, description, owner, theme, genre, country):
    wait_check()
    global is_busy
    is_busy = True
    
    sql = "SELECT EXISTS(SELECT id_servers FROM servers WHERE name = %s)"
    val = (name,)
    cursor.execute(sql, val)
    if(cursor.fetchall()[0][0] != 0):
        is_busy = False
        
        return jsonify({'success':False, 'message':'name'})

    sql = "INSERT INTO servers (name, description, fk_themeid_theme, fk_countryid_country, fk_genreid_genre, fk_usersid_users) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (name, description, theme, country, genre, owner)
    cursor.execute(sql, val)
    mydb.commit()

    sql = "SELECT id_servers FROM servers WHERE name = %s"
    val = (name,)
    cursor.execute(sql, val)

    id = cursor.fetchall()[0][0]

    is_busy = False
        
    return jsonify({'success':True, 'id':id, 'name':name, 'description':description, 'owner':owner, 'theme':theme, 'genre':genre, 'country':country})


def server_delete(id, user_id):
    wait_check()
    global is_busy
    is_busy = True
    
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
                
                is_busy = False
        
                return jsonify({'success':True, 'message':'Server with id: '+id+' , was deleted successfully'})
            else:
                
                is_busy = False
        
                return jsonify({'success':False, 'message':'user_id'})
    else:
        
        is_busy = False
        
        return jsonify({'success':False, 'message':'id'})

def server_edit_info(id, name, description, owner, theme, genre, country):
    wait_check()
    global is_busy
    is_busy = True
    
    sql = "SELECT * FROM servers WHERE id_servers = %s"
    val = (id,)
    cursor.execute(sql, val)
    response = cursor.fetchall()
    if(response[0][0] == 0):
        
        is_busy = False
        
        return jsonify({'success':False, 'message':'id'})
    else:
        for row in response:
            if(row[4] == owner):
                sql = "UPDATE servers SET name = %s, description = %s, fk_themeid_theme = %s, fk_countryid_country = %s, fk_genreid_genre = %s WHERE id_servers = %s"
                val = (name, description, theme, country, genre, id)
                cursor.execute(sql, val)
                mydb.commit()
                
                is_busy = False
        
                return jsonify({'success':True, 'id':id, 'description':description, 'name':name, 'owner':owner, 'theme':theme, 'genre':genre, 'country':country})
            else:
                
                is_busy = False
        
                return jsonify({'success':False, 'message':'user_id'})
            
def server_edit_owner(id, owner, newOwner):
    wait_check()
    global is_busy
    is_busy = True
    
    sql = "SELECT * FROM servers WHERE id_servers = %s"
    val = (id,)
    cursor.execute(sql, val)
    respone = cursor.fetchall()
    if(respone[0][0] == 0):
        is_busy = False
        
        return jsonify({'success':False, 'message':'id'})
    else:
        for row in respone:
            if(row[4] == owner):
                sql = "UPDATE servers SET fk_usersid_users = %s WHERE id_servers = %s"
                val = (newOwner, id)
                cursor.execute(sql, val)
                mydb.commit()

                sql = "SELECT * FROM servers WHERE id_servers = %s"
                val = (id,)
                cursor.execute(sql, val)
                respone = cursor.fetchall()
                for row in respone:
                    
                    is_busy = False
        
                    return jsonify({'success':True, 'id':row[3], 'name':row[0], 'description':row[1], 'users':row[2], 'owner':row[4], 'theme':row[5], 'genre':row[7], 'country':row[6]})
            else:
                
                is_busy = False
        
                return jsonify({'success':False, 'message':'user_id'})
#########################################################################
#DROPDOWN VALUES
#########################################################################

def get_countries():
    wait_check()
    global is_busy
    is_busy = True
    
    sql = "SELECT * FROM country"
    cursor.execute(sql)
    response = cursor.fetchall()
    data = {'success':True}
    data['data'] = []
    tempjson = data['data']
    for row in response:
        tempjson.append({'name':row[0], 'id':row[1]})

    is_busy = False
        
    return jsonify(data)

def get_genres():
    wait_check()
    global is_busy
    is_busy = True
    
    sql = "SELECT * FROM genre"
    cursor.execute(sql)
    response = cursor.fetchall()
    data = {'success':True}
    data['data'] = []
    tempjson = data['data']
    for row in response:
        tempjson.append({'name':row[0], 'id':row[1]})

    is_busy = False
        
    return jsonify(data)

def get_countries_e():
    wait_check()
    global is_busy
    is_busy = True
    
    #SELECT tb1.* FROM tb1 LEFT JOIN tb2 ON tb1.id = tb2.fk_id WHERE tb2.fk_id IS NULL
    sql = "SELECT * FROM country WHERE country.id_country IN (SELECT servers.fk_countryid_country FROM servers)"
    cursor.execute(sql)
    response = cursor.fetchall()
    print(response)
    data = {'success':True}
    data['data'] = []
    tempjson = data['data']
    for row in response:
        tempjson.append({'name':row[0], 'id':row[1]})

    
    is_busy = False
        
    return jsonify(data)


def get_genres_e():
    wait_check()
    global is_busy
    is_busy = True
    
    sql = "SELECT * FROM genre WHERE genre.id_genre IN (SELECT servers.fk_genreid_genre FROM servers)"
    cursor.execute(sql)
    response = cursor.fetchall()
    print(response)
    data = {'success':True}
    data['data'] = []
    tempjson = data['data']
    for row in response:
        tempjson.append({'name':row[0], 'id':row[1]})

    
    is_busy = False
        
    return jsonify(data)

#########################################################################
#ROOM GET DATA
#########################################################################

def get_server_info(id):
    wait_check()
    global is_busy
    is_busy = True
    
    sql = "SELECT EXISTS(SELECT * FROM servers WHERE id_servers = %s)" #"SELECT EXISTS(SELECT * FROM servers WHERE id_servers = %s)"
    val = (int(id),)
    cursor.execute(sql, val)
    response = cursor.fetchall()

    if (response[0][0] == 0):

        print("IN CATCH")
        
        is_busy = False
        
        return jsonify({'success':False, 'message':'id'})
    else:
        sql = "SELECT * FROM servers WHERE id_servers = %s" #"SELECT EXISTS(SELECT * FROM servers WHERE id_servers = %s)"
        val = (int(id),)
        cursor.execute(sql, val)
        response = cursor.fetchall()
        
        for row in response:
            
            is_busy = False
            print(response)
        
            return jsonify({'success':True, 'id':row[3], 'name':row[0], 'description':row[1], 'users':row[2], 'owner':row[4], 'theme':row[5], 'genre':row[7], 'country':row[6]})
    
def get_servers_5(popular, genre, country, offset, limit):
    global db_country
    global db_genre
    
    wait_check()
    global is_busy
    is_busy = True
    
    if limit > 50:
        limit = 50
    
    sql = "SELECT * FROM servers WHERE fk_genreid_genre = %s AND fk_countryid_country = %s ORDER BY users "
    if popular == True:
        sql += "ASC"
    else:
        sql += "DESC"

    sql += " LIMIT %s, %s;"
    val = (genre, country, offset, limit)
    cursor.execute(sql, val)
    response = cursor.fetchall()
    data = {'success':True}
    data['data'] = []
    tempjson = data['data']
    #try:
    for row in response:
        tempjson.append({'name':row[0], 'id':row[3], 'genre':db_genre[row[7]], 'country':db_country[row[6]], 'users':row[2], 'genre_id':row[7], 'country_id':row[6]})


    sql = "SELECT COUNT(*) FROM servers WHERE fk_genreid_genre = %s AND fk_countryid_country = %s"
    val = (genre, country)
    cursor.execute(sql, val)
    items = cursor.fetchall()[0][0]

    dalis = items%limit
    pages = items/limit
    if dalis > 0:
        pages += 1
    
    data['pages'] = pages

    is_busy = False

    return jsonify(data)
    # finally:
        
    #     is_busy = False
        
    #     return jsonify({'success':False, 'message':'null'})

def get_servers_4_2(popular, country, offset, limit):
    global db_country
    global db_genre
    
    wait_check()
    global is_busy
    is_busy = True
    
    if limit > 50:
        limit = 50
    
    sql = "SELECT * FROM servers WHERE fk_countryid_country = %s ORDER BY users "
    if popular == True:
        sql += "ASC"
    else:
        sql += "DESC"

    sql += " LIMIT %s, %s;"
    val = (country, offset, limit)
    cursor.execute(sql, val)
    response = cursor.fetchall()
    data = {'success':True}
    data['data'] = []
    tempjson = data['data']
    for row in response:
        tempjson.append({'name':row[0], 'id':row[3], 'genre':db_genre[row[7]], 'country':db_country[row[6]], 'users':row[2], 'genre_id':row[7], 'country_id':row[6]})

    sql = "SELECT COUNT(*) FROM servers WHERE fk_countryid_country = %s"
    val = (country,)
    cursor.execute(sql, val)
    items = cursor.fetchall()[0][0]

    dalis = items%limit
    pages = items/limit
    if dalis > 0:
        pages += 1
    
    data['pages'] = pages

    is_busy = False
        
    return jsonify(data)
    # finally:
        
    #     is_busy = False
        
    #     return jsonify({'success':False, 'message':'null'})

def get_servers_4_1(popular, genre, offset, limit):
    global db_country
    global db_genre
    
    wait_check()
    global is_busy
    is_busy = True
    
    if limit > 50:
        limit = 50
    
    sql = "SELECT * FROM servers WHERE fk_genreid_genre = %s ORDER BY users "
    if popular == True:
        sql += "ASC"
    else:
        sql += "DESC"

    sql += " LIMIT %s, %s;"
    val = (genre, offset, limit)
    cursor.execute(sql, val)
    response = cursor.fetchall()
    data = {'success':True}
    data['data'] = []
    tempjson = data['data']
    #try:
    for row in response:
        tempjson.append({'name':row[0], 'id':row[3], 'genre':db_genre[row[7]], 'country':db_country[row[6]], 'users':row[2], 'genre_id':row[7], 'country_id':row[6]})

    sql = "SELECT COUNT(*) FROM servers WHERE fk_genreid_genre = %s"
    val = (genre,)
    cursor.execute(sql, val)
    items = cursor.fetchall()[0][0]

    dalis = items%limit
    pages = items/limit
    if dalis > 0:
        pages += 1
    
    data['pages'] = pages


    is_busy = False
        
    return jsonify(data)
    # finally:

    #     is_busy = False
        
    #     return jsonify({'success':False, 'message':'null'})

def get_servers_3(popular, offset, limit):
    global db_country
    global db_genre
    
    wait_check()
    global is_busy
    is_busy = True
    
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
    data = {'success':True}
    data['data'] = []
    tempjson = data['data']
    #try:
    for row in response:
        tempjson.append({'name':row[0], 'id':row[3], 'genre':db_genre[row[7]], 'country':db_country[row[6]], 'users':row[2], 'genre_id':row[7], 'country_id':row[6]})

    print(data)
    print("next to return")

    sql = "SELECT COUNT(*) FROM servers"
    cursor.execute(sql)

    items = cursor.fetchall()[0][0]
    
    dalis = items%limit
    pages = int(items/limit)
    
    if dalis > 0:
        pages += 1
    
    data['pages'] = pages


    is_busy = False

    print("next to return")

    return jsonify(data)
    #finally:
        
        #is_busy = False
        
        #return jsonify({'success':False, 'message':'null'})

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

            return server_add(json.get('name'), json.get('description'), json.get('owner'), json.get('theme'), json.get('genre'), json.get('country'))
        #name, description, owner, theme, genre, country
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

@app.route('/get_server_info', methods=['GET'])
def process_s_info():
    requestType = request.args.get('id', type = int)
    print(requestType)
    if requestType > -1:
        return get_server_info(requestType)
    else:
        return jsonify({'success':False, 'message':'Argument not supported'})

@app.route('/get_servers', methods=['POST'])
def process_servers():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        if isinstance(json.get('popular'), bool) and isinstance(json.get('offset'), int) and isinstance(json.get('limit'), int) and len(json) == 3:
            
            return get_servers_3(json.get('popular'), json.get('offset'), json.get('limit'))

        if isinstance(json.get('popular'), bool) and isinstance(json.get('genre'), int) and isinstance(json.get('country'), int) and isinstance(json.get('offset'), int) and isinstance(json.get('limit'), int) and len(json) == 5:
            
            return get_servers_5(json.get('popular'), json.get('genre'), json.get('country'), json.get('offset'), json.get('limit'))

        if isinstance(json.get('popular'), bool) and isinstance(json.get('genre'), int) and isinstance(json.get('offset'), int) and isinstance(json.get('limit'), int) and len(json) == 4:
            
            return get_servers_4_1(json.get('popular'), json.get('genre'), json.get('offset'), json.get('limit'))

        if isinstance(json.get('popular'), bool) and isinstance(json.get('country'), int) and isinstance(json.get('offset'), int) and isinstance(json.get('limit'), int) and len(json) == 4:
            
            return get_servers_4_2(json.get('popular'), json.get('country'), json.get('offset'), json.get('limit'))

        return jsonify({'success':False, 'message':'JSON keys not supported!'})
    else:
        return jsonify({'success':False, 'message':'Content type not supported'})


getCountryGenre()

if __name__ == "__main__":
    app.run(threaded=True)