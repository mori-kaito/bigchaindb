from pymongo import MongoClient
from datetime import datetime

class TestMongo(object):

    def __init__(self):
         self.clint = MongoClient()
         self.db = self.clint['test']

    def add_one(self):
        """データ挿入"""
        post = {
            'title': 'ハリネズミ',
            'content': 'ハリネズミ可愛い~',
            'created_at': datetime.now()
        }
        return self.db.test.insert_one(post)
    
    def get_one(self):
        return self.db.test.find_one()
    
    def count(self):
        return self.db.test.count_documents(filter={})

def main():
    obj = TestMongo()
    rest = obj.count()
    print(rest)

if __name__ == '__main__':
    main()