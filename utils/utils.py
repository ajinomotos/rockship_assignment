from pymongo import MongoClient

username = "sandbox"
password = "jCDL6tPIvAtomqsF"
dbname = "FBPosts"

uri = f"mongodb+srv://{username}:{password}@cluster0.mzktu.mongodb.net/{dbname}?retryWrites=true&w=majority"

client = MongoClient(uri)
db = client.FBPosts
collection = db.posts

def add_datum(d):
	return collection.insert_one(d).inserted_id

def add_data(documents):
	collection.insert_many(documents)

def find_datum(q):
	return collection.find_one(q)

def delete_datum(d):
	return collection.delete_one(d).deleted_id

def clear_collection():
	return collection.delete_many({}).deleted_count

def count_data():
	return collection.count_documents({})

def show_data():
	c = collection.find({})
	for d in c:
		print(d)