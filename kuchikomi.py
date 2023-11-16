from bigchaindb_driver import BigchainDB
from pymongo import MongoClient
from bigchaindb_driver.crypto import generate_keypair
from datetime import datetime

class kuchikomi(object):

    def __init__(self):
         self.clint = MongoClient()
         self.db = self.clint['kuchikomi']

    def add_one(self, title, text):
        id = self.db.kuchikomi.count_documents(filter={})+1
        """データ挿入"""
        post = {
            'id': id,
            'title': title,
            'content': text,
            'created_at': datetime.now(),
            'delete': 0
        }
        return self.db.kuchikomi.insert_one(post)
    
    def get_one(self, id):
        find = self.db.kuchikomi.find(filter = {'id': id})
        for doc in find:
            print(doc)
    
    def update(self, id, text):
        rest = self.db.kuchikomi.update_one({"id": id}, {"$set": {"content": text, 'created_at': datetime.now()}})
        return rest
    
    def delete(self, id):
        """マッチした最初のデータを削除"""
        rest = self.db.kuchikomi.update_one({"title": id}, {"$set": {"delete": 1}})
        return rest
    
    def count(self):
        return self.db.kuchikomi.count_documents(filter={})

class token(object):

    def __init__(self):
        self.DB = BigchainDB('http://localhost:9984/')

    def createkeypair(self):
        return None

def main():
    obj = kuchikomi()
    # title = input("タイトル：")
    # text = input("口コミの内容：")
    # rest = obj.add_one(title, text)
    # print(rest)
    obj.get_one(1)

if __name__ == '__main__':
    main()

# kaito = generate_keypair()

