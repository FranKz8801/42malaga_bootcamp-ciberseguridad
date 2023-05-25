import random
import datetime
import hashlib
import json
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urllib.parse import urlparse


#from urllib import urlparse

#Empezando el blockchain
class Blockchain:
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(proof=1,previous_hash='0')
        self.nodes = set()
    
    def add_node(self,address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
        

        
    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
                    
        if longest_chain:
            self.chain = longest_chain
            return True
        return False        

    def create_block(self, proof, previous_hash):
        block = {'index':len(self.chain)+1,
                 'timestamp':str(datetime.datetime.now()),
                 'proof':proof,
                 'previous_hash':previous_hash,
                 'transactions':self.transactions}
        
        self.transactions = []
        self.chain.append(block)
        return block
    
    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({'sender':sender, 
                                  'receiver':receiver,
                                  'amount':amount})
        
        previous_block = self.get_previous_block()
        return previous_block['index']+1

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self,previous_proof):
        new_proof = 1
        check_proof = False

        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()

            if hash_operation[:4] == '0000':# and new_proof % len(self.chain) == 0:
                check_proof = True
            #elif hash_operation[:4] == '0000' and datetime.datetime.now().second % 10 == 0:
            #    check_proof = True
            else:
                new_proof += 1
        return new_proof
    def hash(self,block):
        encoded_block = json.dumps(block, sort_keys= True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False

            previous_block = block
            block_index += 1
        return True

#Aplicacion basica en Flask
app = Flask(__name__)

#Creando una Direccion para el Nodo en Puerto 5001
node_address = str(uuid4()).replace('-','')

#Creando  Blockchain
blockchain = Blockchain()

#Minando un Nuevo bloque
@app.route('/mine', methods=['GET'])

def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    
    previous_hash = blockchain.hash(previous_block)
    reward = random.randint(1, 5)
    blockchain.add_transaction(sender= node_address, receiver = 'Loloa', amount=reward)
    block = blockchain.create_block(proof,previous_hash)
    response = {"message": "Felicidades has minado un bloque",
                'index':block['index'],
                'timestamp':block['timestamp'],
                'proof':block['proof'],
                'previous_hash':block['previous_hash'],
                'transactions':block['transactions']}
    return jsonify(response), 200

#Obteniendo cadena completa
@app.route('/chain', methods=['GET'])
def get_chain():
    response = {'chain':blockchain.chain,
                'length':len(blockchain.chain)}
    return jsonify(response), 200

#La valided de la cadena de  bloques 
@app.route('/is_valid', methods=['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'Todo bien. El blockchain es valido.'}
    else:
        response = {'message': 'El Blockchain in es valido.'}
        return jsonify(response), 200



# Agregando nueva transaccion al bloque
@app.route('/new', methods=['POST'])
def add_transaction():
    #json_data = request.get_json()
    #transaction_keys = ['sender', 'receiver', 'amount'] 
    json_data = request.get_json()
    transaction_keys = ['sender', 'receiver', 'amount']
    if not all (key in json_data for key in transaction_keys):
        return 'Algun elemonto de la transacion esta faltando', 400
    index = blockchain.add_transaction(json_data['sender'], json_data['receiver'], json_data['amount'])
    response = {'message':f'La transaccion sera añadida al Bloque {index}'}
    return jsonify(response), 201


# Paso siguiente Descentralizar el Blockchain

#Comentado Nuevos Nodos
@app.route('/connect_nodes', methods=['POST'])
def connect_nodes():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return"No nodes", 401
    for node in nodes:
        blockchain.add_node(node)
    response = {'message': 'Todos los nodos estan ahora conectados. El Coin contiene los siguientes nodos:',
                'total_nodes':list(blockchain.nodes)}
    return jsonify(response), 201


#Remplazando la Cadena por la mas larga
@app.route('/replace_chain', methods=['GET'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {'message': 'Los nodos tenian diferentes cadenas asi que la cadena fue remplazada por la mas larga',
                    'new_chain':blockchain.chain}
    else:
        response = {'message': 'Todo bien, la cadena es la mas larga.',
                    'actual_chain':blockchain.chain}
    return jsonify(response), 200

#Corriendo el App



app.run(host='0.0.0.0', port='5003')