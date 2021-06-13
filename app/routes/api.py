from flask import Blueprint, request, jsonify, session #type:ignore
from app.models import User
from app.db import get_db
import sys

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/users', methods=['POST'])
def signup():
  data = request.get_json()
  db = get_db()
  
  try:
    #create a new user with the login info.
    newUser = User(
      username = data['username'],
      email = data['email'],
      password = data['password']
    )

    #save the new user to the database.
    db.add(newUser)
    db.commit()
  except:
    #print the error to the console to help identify the issue
    print(sys.exc_info()[0])
    #insert failed, so send error to front end
    db.rollback()
    return jsonify(message = 'Signup Failed'), 500

  session.clear()
  session['user_id'] = newUser.id
  session['loggedIn'] = True

  return jsonify(id = newUser.id)

@bp.route('/users/login', methods=['POST'])
def login():
  #login an existing user if they exist in the db
  data = request.get_json()
  db = get_db()
  #check to see if the user exists in the db
  try:
    user = db.query(User).filter(User.email == data['email']).one()
  except:
    print(sys.exc_info()[0])
    return jsonify(message = 'Incorrect Credentials'), 400

  if user.verify_password(data['password']) == False:
    return jsonify(message = 'Incorrect credentials'), 400

  session.clear()
  session['user.id'] = user.id
  session['loggedIn'] = True

  return jsonify(id = user.id)

@bp.route('/users/logout', methods=['POST'])
def logout():
  #remove session variables
  session.clear()
  return '', 204