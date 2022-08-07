from pymongo import MongoClient


client = None
def get_db_client():
    global client
    if client:
        print('client is existing')
        return client

    print('new client is created')
    client =  MongoClient("mongodb+srv://edward:lq1XVk2JDhTsQkl0@cluster0.mutkfdx.mongodb.net/?retryWrites=true&w=majority")
    return client
