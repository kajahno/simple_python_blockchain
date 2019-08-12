#!/usr/bin/env python
import functools
import hashlib
import json
import pickle

from block import Block
from transaction import Transaction
from verification import Verification
from hash_util import hash_block


MINING_REWARD = 10

class Blockchain:
    def __init__(self, hosting_node_id):
        genesis_block = Block(index=0, previous_hash='', transactions=[], proof=100, timestamp=0)
        self.chain = [genesis_block]
        self.__open_transactions = []
        self.load_data()
        self.hosting_node = hosting_node_id

    @property
    def chain(self):
        return self.__chain[:]

    @chain.setter
    def chain(self, val):
        self.__chain = val

    def get_chain(self):
        return self.__chain[:]

    def get_open_transactions(self):
        return self.__open_transactions[:]

    def load_data(self):
        try:
            with open('blockchain.txt','r') as f:
                # file_content = pickle.loads(f.read())
                file_content = f.readlines()

                # blockchain = file_content['chain']
                # open_transactions = file_content['op']
                blockchain = json.loads(file_content[0])
                updated_blockchain = []
                for b in blockchain:
                    transactions = [ Transaction(
                                        sender = t['sender'],
                                        recipient=t['recipient'],
                                        amount=t['amount']) for t in b['transactions'] ]

                    updated_block = Block(index=b['index'],
                                        previous_hash=b['previous_hash'],
                                        transactions=transactions,
                                        proof=b['proof'],
                                        timestamp=b['timestamp'])
                    updated_blockchain.append(updated_block)
                self.chain = updated_blockchain
                open_transactions = json.loads(file_content[1])

                self.__open_transactions = [ Transaction(
                                        sender=t['sender'],
                                        recipient=t['recipient'],
                                        amount=t['amount']) for t in open_transactions ]

        except (FileNotFoundError, IndexError):
            print('Handled exception...')


    def save_data(self):
        with open('blockchain.txt','w') as f:
            blockchain_jsonized = [ Block(index=b.index,
                                        previous_hash=b.previous_hash,
                                        transactions=[ t.__dict__.copy() for t in b.transactions ],
                                        proof=b.proof,
                                        timestamp=b.timestamp ).__dict__.copy() for b in self.__chain ]
            f.write(json.dumps(blockchain_jsonized))
            f.write('\n')
            open_transactions_jsonized = [t.__dict__ for t in self.__open_transactions]
            f.write(json.dumps(open_transactions_jsonized))
            # save_data = {
            #     'chain': blockchain,
            #     'op': open_transactions
            # }
            # f.write(pickle.dumps(save_data))

    def proof_of_work(self):
        last_block = self.__chain[-1]
        last_hash = hash_block(last_block)
        proof = 0
        while not Verification.valid_proof(self.__open_transactions, last_hash, proof):
            proof += 1

        return proof



    def get_balance(self):
        participant = self.hosting_node
        transactions_sent = [ [ transaction.amount for transaction in block.transactions if transaction.sender == participant] for block in self.__chain ]
        open_transactions_sender = [ transaction.amount for transaction in self.__open_transactions if transaction.sender == participant]
        transactions_sent.append(open_transactions_sender)

        amount_sent = 0
        # amount_sent = functools.reduce(lambda tx_sum, tx_amount: tx_sum + tx_amount[0] if len(tx_amount[0]) > 0 else 0, transactions_sent )
        for t in transactions_sent:
            if len(t) > 0:
                amount_sent += sum(t)

        transactions_received = [ [ transaction.amount for transaction in block.transactions if transaction.recipient == participant] for block in self.__chain ]
        amount_received = 0
        for t in transactions_received:
            if len(t) > 0:
                amount_received += sum(t)

        return amount_received - amount_sent


    def get_last_blockchain_value(self):
        if len(self.__chain) == 0:
            return None
        return self.__chain[-1]


    def add_transaction(self, sender, recipient, amount=1.0, reward_transaction=False):
        transaction = Transaction(
                        sender=sender,
                        recipient=recipient,
                        amount=amount)

        if not Verification.verify_transaction(transaction, self.get_balance):
            if reward_transaction:
                print('reward transaction detected')
            else:
                return False

        self.__open_transactions.append(transaction)
        self.save_data()
        return True


    def mine_block(self):
        last_bock = self.__chain[-1]
        hash_val = hash_block(last_bock)

        proof_of_work_number = self.proof_of_work()
        print(hash_val)
        # add_transaction(sender='MINING', recipient=owner, amount=MINING_REWARD, reward_transaction=True)

        reward_transaction = Transaction(
                                sender='MINING',
                                recipient=self.hosting_node,
                                amount=MINING_REWARD)

        copied_transactions = self.__open_transactions[:]
        copied_transactions.append(reward_transaction)

        block = Block(index=len(self.__chain),
                    previous_hash=hash_val,
                    transactions=copied_transactions,
                    proof=proof_of_work_number)
        self.__chain.append(block)
        self.__open_transactions = []
        self.save_data()
        return True


