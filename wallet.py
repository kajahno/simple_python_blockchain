from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import Crypto.Random
import binascii

class Wallet:
    def __init__(self):
        self.private_key = None
        self.public_key = None

    def create_keys(self):
        private_key, public_key = self.generate_keys()
        self.private_key = private_key
        self.public_key = public_key


    def save_keys(self):
        if self.public_key is None or self.private_key is None:
            print("Cannot save empty keys...")
            return

        try:
            with open('wallet.txt', mode='w') as f:
                f.write(self.public_key)
                f.write('\n')
                f.write(self.private_key)
        except (IOError, IndexError):
            print('Saving key failed...')


    def load_keys(self):
        try:
            with open('wallet.txt', mode='r') as f:
                public_key, private_key = f.read().split('\n')
                self.public_key = public_key
                self.private_key = private_key
        except (IOError, IndexError):
            print('Loading wallet failed...')


    def generate_keys(self):
        private_key = RSA.generate(2048, Crypto.Random.new().read)
        public_key = private_key.publickey()
        private_key_ascii = binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii')
        public_key_ascii = binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii')

        return (private_key_ascii, public_key_ascii)

    def sign_transaction(self, sender, recipient, amount):
        private_key_bin = binascii.unhexlify(self.private_key)
        signer = PKCS1_v1_5.new(RSA.importKey(private_key_bin))

        pre_hash_str = (str(sender) + str(recipient) + str(amount)).encode('utf-8')
        h = SHA256.new(pre_hash_str)
        signature = signer.sign(h)

        return binascii.hexlify(signature).decode('ascii')

    @staticmethod
    def verify_transaction(transaction):
        public_key = RSA.importKey(binascii.unhexlify(transaction.sender))
        verifier = PKCS1_v1_5.new(public_key)
        pre_hash_str = (str(transaction.sender)
                        + str(transaction.recipient)
                        + str(transaction.amount)).encode('utf-8')
        h = SHA256.new(pre_hash_str)

        return verifier.verify(h, binascii.unhexlify(transaction.signature))

