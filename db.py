import pymongo
dbuser='ram'
dbpassword='ramu4321'

db_name='ram'
db_url="mongodb+srv://{}:{}@cluster0.rgmj5.gcp.mongodb.net/?retryWrites=true&w=majority".format(dbuser,dbpassword)
db = pymongo.MongoClient(db_url).ram

def store_search_history(search_query, author):
	db.history.insert_one({'keyword':search_query, "user":author.name})
	return True
def get_history_keyword(query, author):
	word_search = query.strip().split(' ')
	keyword_history_list = list()
	for word in word_search:
		history=db.history.find_one({'keyword':{'$regex':word}, "user":author.name})
		if history and history.get('keyword') not in keyword_history_list :
			keyword_history_list.append('`{}`'.format(history.get('keyword')))
	if not keyword_history_list:
		return None
	return"you have searched these keywords: \n"+"\n".join(keyword_history_list)
