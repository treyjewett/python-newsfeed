from flask import Blueprint, request, jsonify #type:ignore
from app.models import User
from app.db import get_db

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/users', methods=['POST'])
def signup():
  data = request.get_json()
  db = get_db()
  
  #create a new user with the login info.
  newUser = User(
    username = data['username'],
    email = data['email'],
    password = data['password']
  )

  #save the new user to the database.
  db.add(newUser)
  db.commit()

  return jsonify(id = newUser.id)