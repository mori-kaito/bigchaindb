from bigchaindb_driver import BigchainDB
from pymongo import MongoClient
from bigchaindb_driver.crypto import generate_keypair
from datetime import datetime

class kuchikomi(object):

    def __init__(self):
        self.clint = MongoClient()
        self.db = self.clint['kuchikomi']

    def add_one(self, name, title, text):
        id = self.db.kuchikomi.count_documents(filter={})+1
        """データ挿入"""
        post = {
            'id': id,
            'user_name': name,
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
    
class medical(object):

    def __init__(self):
        self.clint = MongoClient()
        self.db = self.clint['medical']

    def add_one(self, name):
        id = self.db.medical.count_documents(filter={})+1
        """データ挿入"""
        post = {
            'id': id,
            'patient_name': name,
            'data': None,
            'created_at': datetime.now(),
            'delete': 0
        }
        return self.db.kuchikomi.insert_one(post)
    
    def get_one(self, id):
        find = self.db.kuchikomi.find(filter = {'id': id})
        for doc in find:
            print(doc)


class transaction(object):

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
    
    def return_check(self, fulfilled_creation_tx):
        block_height = self.DB.blocks.get(txid=fulfilled_creation_tx['id'])
        block = self.DB.blocks.retrieve(str(block_height))
        print(block_height)
        print(block)

def main():
    obj_k = kuchikomi()
    # u_name = input("username: ")
    # title = input("タイトル：")
    # text = input("口コミの内容：")
    # rest = obj_k.add_one(u_name, title, text)
    # print(rest)
    obj_k.get_one(2)

    obj_m = medical()
    # p_name = input("名前: ")
    # rest = obj_m.add_one(p_name)
    # print(rest)
    obj_m.get_one(1)

    obj_t = transaction()

    # 仮の変数
    test_name = "kaito"

    username = obj_t.createkeypair(test_name)

    # 固定した変数
    kuchikomi_id = 2
    medical_id = 1
    title = "test"
    
    kuchikomi_asset = obj_t.create_asset(kuchikomi_id, medical_id, title)
    prepared_creation_tx = obj_t.prepared_creation_tx(username, kuchikomi_asset)
    fulfilled_creation_tx = obj_t.fulfilled_creation_tx(prepared_creation_tx, username)
    obj_t.tx_commit(fulfilled_creation_tx)
    print(obj_t.tx_id(fulfilled_creation_tx))

    obj_t.return_check(fulfilled_creation_tx)


if __name__ == '__main__':
    main()

# kaito = generate_keypair()

