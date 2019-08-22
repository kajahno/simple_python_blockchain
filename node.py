#!/usr/bin/env python

from uuid import uuid4

from blockchain import Blockchain
from utility.verification import Verification
from wallet import Wallet

class Node:

    def __init__(self):
        self.wallet = Wallet()
        self.blockchain = Blockchain(self.wallet.public_key)


    def get_transaction_value(self):
        recipient = input('Enter the recipient of the transaction: ')
        amount  = float(input('Your transaction amount please: '))
        return recipient, amount


    def get_user_choice(self):
        user_input = input('Your choice: ')
        return user_input


    def print_blockchain_elements(self):
        for block in self.blockchain.chain:
            print('Outputting block: {}'.format(block))
        else:
            print('-' * 20)


    def listen_for_input(self):
        waiting_for_input = True

        while waiting_for_input:
            print("""
            Please choose:
                1) Add a new transaction value
                2) Mine a new block
                3) Output the blockchain blocks
                4) Check transaction validity
                5) Create wallet
                6) Load keys
                7) Save keys
                q: Quit
            """)
            user_choice = self.get_user_choice()
            if user_choice == '1':
                recipient, amount = self.get_transaction_value()
                signature = self.wallet.sign_transaction(sender=self.wallet.public_key,
                                recipient=recipient,
                                amount=amount)
                if self.blockchain.add_transaction(sender=self.wallet.public_key, recipient=recipient, amount=amount, signature=signature):
                    print('Added transaction')
                else:
                    print('Transaction failed')
                # print(open_transactions)
            elif user_choice == '2':
                if not self.blockchain.mine_block():
                    print("Mining failed. Got no wallet?")
            elif user_choice == '3':
                self.print_blockchain_elements()
            elif user_choice == '4':
                if Verification.verify_transactions(self.blockchain.get_open_transactions(), self.blockchain.get_balance):
                    print('all transaction are valid')
                else:
                    print('there are invalid transactions')
            elif user_choice == '5':
                self.wallet.create_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
            elif user_choice == '6':
                self.wallet.load_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
            elif user_choice == '7':
                self.wallet.save_keys()
            elif user_choice == 'q':
                waiting_for_input = False
            else:
                print('invalid input, choose a value from the list')

            print("Balance of {}: {:6.2f}".format(self.wallet.public_key, self.blockchain.get_balance()))

            if not Verification.verify_chain(self.blockchain.chain):
                self.print_blockchain_elements()
                print('invalid blockchain!')
                break


if __name__ == "__main__":
    node = Node()
    node.listen_for_input()
