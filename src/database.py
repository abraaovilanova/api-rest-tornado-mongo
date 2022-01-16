import pymongo

def db_connect(collection="employees"):
	"""
	Return a db connection
	"""
	myclient = pymongo.MongoClient("mongodb://localhost:27017/")
	mydb = myclient["mydatabase"]
	
	mycol = mydb[collection]
	return mycol