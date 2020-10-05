from flask import Flask
from flask import jsonify
from flask import request
import pymongo
import re


api = Flask(__name__)
api.config["DEBUG"] = True

username = "sandbox"
password = "jCDL6tPIvAtomqsF"
dbname = "FBPosts"

uri = f"mongodb+srv://{username}:{password}@cluster0.mzktu.mongodb.net/{dbname}?retryWrites=true&w=majority"

client = pymongo.MongoClient(uri)
db = client.FBPosts


# API to search for term in appears in facebook post stored in mongodb database
# Facebook posts default fields:
#		_id  :  id of post
#		message : content of the post
#		created_time : timestampt of the post
#
# Sample request: GET http://127.0.0.1:5000/posts/search?q=<search_term>	: none exact match
#				  GET http://127.0.0.1:5000/posts/search?q=<search_term>&exact_match=True   : exact match
#	
# Return: {'data': [
# 					'content': <matched message>,
# 					'content': <matched message>,...]}
@api.route('/posts/search', methods=['GET'])
def search():
	out = {"data": []}
	search_term = request.args.get('q')

	exact = False
	exact_match = request.args.get('exact_match')
	if exact_match == "True":
		exact = True

	# Bad request
	if not search_term:
		return "No search term", 400

	if exact:
		regex = re.compile("\\b" + search_term + "\\b", re.IGNORECASE)
	else:
		regex = re.compile(search_term, re.IGNORECASE)

	for d in db.posts.find({"message": regex}):
		out["data"].append({"content" : d["message"]})

	return jsonify(out), 200