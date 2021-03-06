#!/usr/bin/env python

import MySQLdb
import MySQLdb.cursors

name = "jarrylsubang"

def get_db(psw):
    db = MySQLdb.connect(
        host = "img-repo-db.czwcl89wj6vg.us-east-2.rds.amazonaws.com",
        port = 3306,
        user = "admin",
        passwd = psw,
        db = "testdb")
    return db

##### General db functions #####

# Deletes an entry from a table
def del_record(column, value, table):
    # connect to db
    db = get_db(name)
    cursor = db.cursor()

    del_cmd = "DELETE FROM {0} WHERE {1} = '{2}'".format(table, column, value)
    cursor.execute(del_cmd)
    db.commit()

    # disconnect from db
    cursor.close()
    db.close()
    return

# Gets a user from the database if it exists, Returns None if user is not found 
def get_record(column, value, table):

    # connect to db
    db = get_db(name)
    cursor = db.cursor()

    sel_cmd = "SELECT * FROM {0} WHERE {1} = '{2}'".format(table, column, value)
    cursor.execute(sel_cmd)
    result = None    
    result = cursor.fetchone()

    # disconnect from db
    cursor.close()
    db.close()

    return result


###### functions for user table #####

# Adds a user to the database, returns True if successful, False if the add failed
def add_user(username, password):

    # connect to db
    db = get_db(name)
    cursor = db.cursor()

    # if username exists, cancel
    if (get_record('username', username, 'user') != None):

        # disconnect from db
        cursor.close()
        db.close()
        return False

    insert = "INSERT INTO user (username, password) VALUES (%s, %s)"
    values = (username, password)
    cursor.execute(insert, values)
    db.commit()

    # disconnect from db
    cursor.close()
    db.close()

    return True

# Edits a attribute for a user
def edit_user(col, value, user_id):

    # connect to db
    db = get_db(name)
    cursor = db.cursor()

    edit_cmd = "UPDATE user SET {0} = '{1}' WHERE user_id = '{2}'".format(col, value, user_id)
    cursor.execute(edit_cmd)
    db.commit()

    # disconnect from db
    cursor.close()
    db.close()

    return

# gets the user_id associated with a username from the server, returns -1 if id is not found
def get_user_id(username):
    
    user_id = ""
    record = get_record("username", username, "user")

    if(record == None):
        user_id = -1 
    else:
        user_id = record[0]   
        
    return user_id

# gets the user password from the database, returns a blank if username does not exist in the database 
def get_user_password(username):
    password = ""
    record = get_record("username", username, "user")

    if(record == None):
        password = "" 
    else:
        password = record[2]   

    return password


# checks the user credentials, returns True if credentials are correct, false otherwise
def check_credentials(username, password):

    # get_user password
    db_pass = get_user_password(username)

    # return false if username is not in the database
    if(db_pass == ""):
        return False

    # compare database password with proposed password
    if (password == db_pass):
        return True
    else:
        return False


##### functions for image table #####
def add_image(user_id, filename, filetype, private):

    # connect to db
    db = get_db(name)
    cursor = db.cursor()

    insert = "INSERT INTO image (user_id, filename, filetype, private) VALUES ({0}, '{1}', '{2}', {3})".format(user_id, filename, filetype, private)
    cursor.execute(insert)
    db.commit()

    # disconnect from db
    cursor.close()
    db.close()

    return True


# gets the owner of an image with the inputted id, returns -1 if image is not in tha database
def get_image_owner(id):
    owner = -1
    record = get_record("file_id", id, "image")

    if(record == None):
        owner = -1
    else:
        owner = record[1]

    return owner

# Gets all the image records from the database
def get_all_images():

    # connect to db
    db = get_db(name)
    cursor = db.cursor()

    sel_cmd = "SELECT * FROM image"
    cursor.execute(sel_cmd)  
    result = cursor.fetchall()

    # close db connection
    cursor.close()
    db.close()

    if(result == None):
        result = ()

    return result

# gets the id number that will correspond to the filename in the uploads directory, returns a -1 if not found
def get_image_id(user_id, filename):

    # open connection
    db = get_db(name)
    cursor = db.cursor()

    user_condition = "user_id = {0}".format(user_id)
    file_condition = "filename = '{0}'".format(filename)
    sel_cmd = "SELECT DISTINCT file_id FROM image WHERE {0} AND {1}".format(user_condition, file_condition)
    cursor.execute(sel_cmd)
    result = cursor.fetchone()

    # close connection
    cursor.close()
    db.close()

    if(result == None):
        result = -1
        return result
    else:
        return result[0]
    # return -11

# get the file extension of the image from the database, returns the type or "" if not found
def get_image_type(file_id):

    # open connection
    db = get_db(name)
    cursor = db.cursor()

    sel_cmd = "SELECT DISTINCT filetype FROM image WHERE file_id = {0}".format(file_id)
    cursor.execute(sel_cmd)
    result = () 
    result = cursor.fetchone()

    # close connection
    cursor.close()
    db.close()

    if(result == None):
        result = ""
    else:
        return result[0]

#deletes image record, returns true if record was removed, false otherwise
def del_image_record(image_id):

    # open connection
    db = get_db(name)
    cursor = db.cursor()

    del_cmd = "DELETE FROM image WHERE file_id = {0}".format(image_id)
    cursor.execute(del_cmd)
    db.commit()

    # close connection
    cursor.close()
    db.close()

    return