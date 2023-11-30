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

    def createkeypair(self, user_name):
        user_name = generate_keypair()
        return user_name
    
    def create_asset(self, kuchikomi_id, medical_id, title):
        kuchikomi_asset = {
            'data': {
                title: {
                    'kuchikomi_id': kuchikomi_id,
                    'medical_id' : medical_id
                }
            }
        }
        return kuchikomi_asset
    
    def prepared_creation_tx(self, user_name, kuchikomi_asset):
        prepared_creation_tx = self.DB.transactions.prepare(
            operation='CREATE',
            signers=user_name.public_key,
            asset=kuchikomi_asset
        )
        return prepared_creation_tx
    
    def fulfilled_creation_tx(self, prepared_creation_tx, user_name):
        fulfilled_creation_tx = self.DB.transactions.fulfill(
            prepared_creation_tx,
            private_keys=user_name.private_key
        )
        return fulfilled_creation_tx
    
    def tx_commit(self, fulfilled_creation_tx):
        sent_creation_tx = self.DB.transactions.send_commit(fulfilled_creation_tx)
        print(sent_creation_tx==fulfilled_creation_tx)

    def tx_id(self, fulfilled_creation_tx):
        txid = fulfilled_creation_tx['id']
        return txid

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

