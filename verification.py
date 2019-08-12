from hash_util import hash256_string, hash_block


class Verification:

    @staticmethod
    def valid_proof(transactions, last_hash, proof_of_work_number):
        guess_str = str([t.to_ordered_dict() for t in transactions]) + str(last_hash) + str(proof_of_work_number)
        print(f"guess_str={guess_str}.")
        guess_str = guess_str.encode()
        guess_hash = hash256_string(guess_str)
        # print(guess_hash)
        return guess_hash[0:2] == '00'

    @classmethod
    def verify_chain(cls, blockchain):
        is_valid = True
        for idx, block in enumerate(blockchain):
            if idx == 0:
                continue
            if block.previous_hash != hash_block(blockchain[idx - 1]):
                is_valid = False
                break
            if not cls.valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
                print('proof of work is invalid')
                is_valid = False
                break
        return is_valid

    @staticmethod
    def verify_transaction(transaction, get_balance):
        sender_balancer = get_balance()
        return sender_balancer >= transaction.amount

    @classmethod
    def verify_transactions(cls, open_transactions, get_balance):
        return all([cls.verify_transaction(transaction, get_balance) for transaction in open_transactions])
