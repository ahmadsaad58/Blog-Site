from flask import Flask, g
from flask_restful import Resource, Api, reqparse
import os
import shelve


# Create an instance of Flask
app = Flask(__name__)

# Create the API
api = Api(app)

# Get my Database
def get_db():
	# TODO: use better DB
	db = getattr(g, 'my_database', None)
	if db is None:
		db = g.my_database = shelve.open('posts.db')
	return db

# Teardown
@app.teardown_appcontext
def teardown_db(exception):
	# TODO: use better DB
    db = getattr(g, 'my_database', None)
    if db is not None:
        db.close()


@app.route('/')
def index():
	# TODO: Link to Static Page
	return 'Hello User'

@app.route('/help')
def debug():
	# TODO: Link to static Page
	return 'Help is on the way'


class Blog_List(Resource):
	# Get all blogs
	def get(self):
		my_shelf = get_db()
		blogs = [my_shelf[key] for key in my_shelf.keys()]
		return {'message': 'Success', 'data': blogs}, 200

	# add a blog
	def post(self):
		parser = reqparse.RequestParser()

		parser.add_argument('identifier', required=True)
		parser.add_argument('title', required=True)
		parser.add_argument('author', required=True)

		args = parser.parse_args()

		shelf = get_db()
		shelf[args['identifier']] = args

		return {'message': "Blog Added", "data": args}, 201



class Blog(Resource):
	# Get a single Blog
	def get(self, identifier):
		shelf = get_db()

		if identifier not in shelf: 
			return {'message': 'Blog not found', 'data': {}}, 404
		
		return {'message': 'Blog found', 'data': shelf[identifier]}, 200

	# Delete a Single Blog
	def delete(self, identifier):
		shelf = get_db()
		
		if identifier not in shelf:
			return {'message': 'Blog not found', 'data': {}}, 404
		
		del shelf[identifier]
		return '', 204


api.add_resource(Blog_List, '/blogs')
api.add_resource(Blog, '/blog/<string:identifier>')





