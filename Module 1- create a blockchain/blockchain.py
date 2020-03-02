# module 1 - create a blockchain

import datetime
import hashlib
import json
from flask import Flask, jsonify

#building BLOCKCHAIN
class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(prev_hash='0'*64)
        
    def create_block(self, prev_hash):
        block = {
                    'index':len(self.chain)+1,
                    'timestamp': str(datetime.datetime.now()),
                    'previous_hash': prev_hash
                }
        block = self.proof_of_work(block)
        self.chain.append(block)
        return block
    
    
    def get_prev_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, block):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = self.hash(block)
            
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
            block['proof'] = new_proof
        return block
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        prev_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(prev_block):
                return False
            prev_proof = prev_block['proof']
            proof = block['proof']
            
            hash_operation = self.hash(block)
            print(hash_operation)
            if hash_operation[:4] != '0000':
                return False
            prev_block = block
            block_index += 1
        return True
    
    
#MINING OUR BLOCKCHAIN
        
#CREATING A WEBAPP
app = Flask(__name__)

blockchain = Blockchain()

@app.route('/mine_block', methods=['GET'])
def mine_block():
    prev_block = blockchain.get_prev_block()
    prev_hash = blockchain.hash(prev_block)
    block = blockchain.create_block(prev_hash)
    response = {
                'msg':'Congrats, Block mined successfully!',
                'index': block['index'],
                'timestamp':block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']
                }
    return jsonify(response), 200

@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {
                'chain': blockchain.chain,
                'length': len(blockchain.chain)
            }
    
    return jsonify(response), 200

@app.route('/is_valid', methods=['GET'])
def isValid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        return jsonify({'msg':'chain is valid'}), 200
    else:
        return jsonify({'msg':'chain is invalid'}), 200
app.run(host = '0.0.0.0',port=5000)