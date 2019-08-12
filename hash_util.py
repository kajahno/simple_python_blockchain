import hashlib
import json

def hash256_string(string):
    return hashlib.sha256(string).hexdigest()

def hash_block(block):
    block_dict = block.__dict__.copy()
    block_dict['transactions'] = [ t.to_ordered_dict() for t in block_dict['transactions'] ]
    block_str = json.dumps(block_dict, sort_keys=True).encode()
    block_hashed = hash256_string(block_str)
    return block_hashed
