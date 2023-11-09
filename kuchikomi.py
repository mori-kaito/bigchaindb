from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair

conn = BigchainDB('http://localhost:9984/')

nameSpace = 'rbac-bdb-kuchikomi'
async def createApp():
    admin = generate_keypair()

    adminGroupAsset = conn.transactions.prepare(
        operation='CREATE',
        signers=admin.public_key,
    )

