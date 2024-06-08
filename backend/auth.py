import functools
import time
from flask import (
	Blueprint, flash ,g , redirect, render_template,request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db

bp = Blueprint('auth',__name__,url_prefix='/auth')

@bp.route('/register', methods=('GET','POST'))
def register():
	if request.method=='POST':
		# section to change as to make it an API
		username = request.json['username']
		password = request.json['password']
		user_role = 1
		db = get_db()
		error = None

		if not username:
			error = {'status': 300, 'message': 'Username is required' }
		elif not password:
			error = {'status': 300,'message': 'Password is required'}
		elif db.execute(
			'SELECT u_id FROM user WHERE username = ?',(username,)
		).fetchone() is not None:
			error = {'status': 300 ,'message':'User {} is already registered.'.format(username)}
		
		if error is None:
			db.execute(
				'INSERT INTO user (username,password,user_role) VALUES (?,?,?)',
				(username,generate_password_hash(password),user_role)
			)
			db.commit()
			msg = {'status':200, 
				'message': 'User {} is successfully registered'.format(username)
			}
			#return redirtect(url_for('auth.login'))
		#flash(error)
		response = {
				'is_Succesful': True if error is None else False,
  				'message': msg if error is None else error
			}
	return response

@bp.route('/login',methods=('GET','POST'))
def login():
	if request.method == 'POST':
		# to change for api
		username = request.json['username']
		password = request.json['password']
		db = get_db()
		error = None
		user = db.execute(
			'SELECT * FROM  user WHERE username = ?',(username,)
		).fetchone()

		if user is None:
			error = {'status':300,'message':'Incorrect username'}
		elif not check_password_hash(user['password'],password):
			error = {'status':300, 'message':'Incorrect Password'}
		
		if error is None:
			timestamp = time.ctime()
			authkey = generate_password_hash(user['username']+timestamp)
			message = {'status': 200,'auth_Key':authkey,'user': user['username'], 'timestamp': timestamp, 'message':'Successfully authorized'}
		response = {
				'is_Successful': True if error is None else False,
				'response' : message if error is None else error
			}
	return response

@bp.route('/validate',methods=('GET','POST'))
def validation():
	if request.method == 'POST':
		# to change for api
		response = request.json['response']
		error = None
		if not check_password_hash(response['auth_Key'],response['user']+response['timestamp']):
			error = {'status':404}
		else:
			resp = {'status':200}
		response = {
				'is_Successful': True if error is None else False,
				'response' : resp if error is None else error
		}
	return response
	
@bp.route('/logout',methods=('GET','POST'))
def logout():
	authkey = None
	return {'status':200,'message':'reset authkey'}