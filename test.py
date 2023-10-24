from bigchaindb_driver import BigchainDB
bdb_root_url = 'http://localhost:9984'

tokens = {'app_id': 'your_app_id', 'app_key': 'your_app_key'}
bdb = BigchainDB(bdb_root_url, headers=tokens)

bicycle = {
    'data': {
        'bicycle': {
           'serial_number': 'abcd1234',
            'manufacturer': 'bkfab',
        },
    },
}

metadata = {'planet': 'earth'}

from bigchaindb_driver.crypto import generate_keypair
alice, bob = generate_keypair(), generate_keypair()

prepared_creation_tx = bdb.transactions.prepare(
    operation='CREATE',
    signers=alice.public_key,
    asset=bicycle,
    metadata=metadata,
)

# print(prepared_creation_tx)