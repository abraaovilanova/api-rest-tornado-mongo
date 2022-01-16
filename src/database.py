import pymongo

def db_connect(collection="employees"):
	myclient = pymongo.MongoClient("mongodb://localhost:27017/")
	mydb = myclient["mydatabase"]
	
	mycol = mydb[collection]
	return mycol