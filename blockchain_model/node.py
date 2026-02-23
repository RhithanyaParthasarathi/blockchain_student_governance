import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4
import httpx
import asyncio

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import sys
import os

class Blockchain:
    def __init__(self, port):
        self.port = port
        self.chain = []
        self.current_transactions = []
        self.nodes = set()
        self.storage_file = f"chain_{self.port}.json"
        
        # Try to load existing chain
        self.load_chain()
        
        # Create the genesis block if chain is empty
        if not self.chain:
            self.new_block(previous_hash='1', proof=100)

    def load_chain(self):
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as f:
                    data = json.load(f)
                    self.chain = data.get('chain', [])
            except json.JSONDecodeError:
                pass
                
    def save_chain(self):
        with open(self.storage_file, 'w') as f:
            json.dump({'chain': self.chain}, f, indent=4)

    def register_node(self, address):
        """
        Add a new node to the list of nodes
        :param address: Address of node. Eg. 'http://127.0.0.1:5000'
        """
        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            # Accepts an URL without scheme like '192.168.0.5:5000'.
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError('Invalid URL')

    def valid_chain(self, chain):
        """
        Determine if a given blockchain is valid
        :param chain: A blockchain
        :return: True if valid, False if not
        """
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            # Check that the hash of the block is correct
            last_block_hash = self.hash(last_block)
            if block['previous_hash'] != last_block_hash:
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block['proof'], block['proof'], last_block_hash):
                return False

            last_block = block
            current_index += 1

        return True

    async def resolve_conflicts(self):
        """
        This is our consensus algorithm, it resolves conflicts
        by replacing our chain with the longest one in the network.
        :return: True if our chain was replaced, False if not
        """
        neighbors = self.nodes
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        async with httpx.AsyncClient() as client:
            for node in neighbors:
                try:
                    response = await client.get(f'http://{node}/chain')
                    
                    if response.status_code == 200:
                        length = response.json()['length']
                        chain = response.json()['chain']

                        # Check if the length is longer and the chain is valid
                        if length > max_length and self.valid_chain(chain):
                            max_length = length
                            new_chain = chain
                except Exception as e:
                    print(f"Error connecting to {node}: {e}")

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            self.save_chain()
            return True

        return False

    def new_block(self, proof, previous_hash=None):
        """
        Create a new Block in the Blockchain
        :param proof: The proof given by the Proof of Work algorithm
        :param previous_hash: Hash of previous Block
        :return: New Block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        self.save_chain()
        return block

    def new_transaction(self, voter_id, candidate_id):
        """
        Creates a new transaction to go into the next mined Block
        :param voter_id: Address of the Voter
        :param candidate_id: Address/ID of the Candidate
        :return: The index of the Block that will hold this transaction
        """
        self.current_transactions.append({
            'voter_id': voter_id,
            'candidate_id': candidate_id,
        })
        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block
        :param block: Block
        """
        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_block):
        """
        Simple Proof of Work Algorithm:
         - Find a number p' such that hash(pp') contains leading 4 zeroes
         - Where p is the previous proof, and p' is the new proof
        """
        last_proof = last_block['proof']
        last_hash = self.hash(last_block)

        proof = 0
        while self.valid_proof(last_proof, proof, last_hash) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof, last_hash):
        """
        Validates the Proof
        :param last_proof: Previous Proof
        :param proof: Current Proof
        :param last_hash: The hash of the Previous Block
        :return: True if correct, False if not.
        """
        guess = f'{last_proof}{proof}{last_hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"


# Instantiate the Node
app = FastAPI(title="Student Governance Blockchain Node")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get port from args or env to manage multi-node setup
port = int(os.environ.get('PORT', 5000))

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain(port)


class TransactionModel(BaseModel):
    voter_id: str
    candidate_id: str

class NodesModel(BaseModel):
    nodes: List[str]

@app.get('/mine')
async def mine():
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block)

    # We must receive a reward for finding the proof.
    # We can omit the reward for a private voting system, 
    # but let's keep it structurally similar to a real chain.
    # blockchain.new_transaction(
    #     sender="0",
    #     recipient=node_identifier,
    #     amount=1,
    # )

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    # Broadcast the new block to all nodes (Gossip-style)
    neighbors = blockchain.nodes
    async with httpx.AsyncClient() as client:
        for node in neighbors:
            try:
                await client.get(f'http://{node}/nodes/resolve')
            except Exception as e:
                print(f"Error notifying {node}: {e}")

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return response

@app.post('/transactions/new')
def new_transaction(transaction: TransactionModel):
    # Create a new Transaction
    index = blockchain.new_transaction(transaction.voter_id, transaction.candidate_id)
    response = {'message': f'Transaction will be added to Block {index}'}
    return response

@app.get('/transactions/pending')
def pending_transactions():
    return {
        'transactions': blockchain.current_transactions
    }

@app.get('/chain')
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return response

@app.post('/nodes/register')
def register_nodes(nodes_input: NodesModel):
    nodes = nodes_input.nodes

    if nodes is None:
        raise HTTPException(status_code=400, detail="Error: Please supply a valid list of nodes")

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return response

@app.get('/nodes/resolve')
async def consensus():
    replaced = await blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }
    return response

@app.get('/')
def home():
    return {"message": f"Blockchain node running on port {port}"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=port)
