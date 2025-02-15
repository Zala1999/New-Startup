import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

import bson

from flask import current_app, g
from werkzeug.local import LocalProxy
from flask_pymongo import PyMongo
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, OperationFailure
from bson.objectid import ObjectId
from bson.errors import InvalidId


def get_db_mongo(ATLAS_URI='', DB_NAME=''):
	"""
	Configuration method to return db instance
	"""
	if 'db' in g:
		db = getattr(g, "_database", None)
		if db is None:
			db = g._database = PyMongo(current_app).db
		return db
	elif ATLAS_URI=='' or DB_NAME == '':
		raise OperationFailure('Connection Failure, please use ATLAS_URI and DB_NAME properly')
	else:
		client = MongoClient(ATLAS_URI)
		db = client[DB_NAME]
		return db



def get_db():
	if 'db' not in g:
		g.db = sqlite3.connect(
			current_app.config['DATABASE'],
			detect_types=sqlite3.PARSE_DECLTYPES
		)
		g.db.row_factory = sqlite3.Row
	return g.db

def close_db(e=None):
	db = g.pop('db',None)

	if db is not None:
		db.close()


def init_db():
	db = get_db()
	with current_app.open_resource('schema.sql') as f:
		db.executescript(f.read().decode('utf8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
	'''
	Clear existing data and create new tables
	WARNING :  Executing it will delete Existing rows!
	'''
	init_db()
	click.echo('Initialized the database.')

def init_app(app):
	app.teardown_appcontext(close_db)
	app.cli.add_command(init_db_command)

# Use LocalProxy to read the global db instance with just `db`
db = LocalProxy(get_db_mongo)

