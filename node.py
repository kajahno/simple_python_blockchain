#!/usr/bin/env python

from uuid import uuid4

from blockchain import Blockchain
from verification import Verification


class Node:

    def __init__(self):
        # self.id = str(uuid4())
        self.id = 'Karl'
        self.blockchain = Blockchain(self.id)

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
            print("Balance of {}: {:6.2f}".format(self.id, self.blockchain.get_balance()))
            print("""
            Please choose:
                1) Add a new transaction value
                2) Mine a new block
                3) Output the blockchain blocks
                4) Check transaction validity
                q: Quit
            """)
            user_choice = self.get_user_choice()
            if user_choice == '1':
                recipient, amount = self.get_transaction_value()
                if self.blockchain.add_transaction(sender=self.id, recipient=recipient, amount=amount):
                    print('Added transaction')
                else:
                    print('Transaction failed')
                # print(open_transactions)
            elif user_choice == '2':
                self.blockchain.mine_block()
            elif user_choice == '3':
                self.print_blockchain_elements()
            elif user_choice == '4':
                if Verification.verify_transactions(self.blockchain.get_open_transactions(), self.blockchain.get_balance):
                    print('all transaction are valid')
                else:
                    print('there are invalid transactions')
            elif user_choice == 'q':
                waiting_for_input = False
            else:
                print('invalid input, choose a value from the list')


            if not Verification.verify_chain(self.blockchain.chain):
                self.print_blockchain_elements()
                print('invalid blockchain!')
                break


if __name__ == "__main__":
    node = Node()
    node.listen_for_input()
