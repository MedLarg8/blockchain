import hashlib
import random
import string
import json
import binascii
import Cryptodome.Random
import numpy as np
import pandas as pd
import pylab as pl
import logging
import datetime
import collections

import Cryptodome
import Cryptodome.Hash
from Cryptodome.Hash import SHA
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import PKCS1_v1_5
from hashlib import sha256

tp_coins=[]
LAST_BLOCK_HASH = ""
LAST_TRANSACTION_INDEX = 0


def dump_blockchain(self):
        print("number of blocks in the chain : "+str(len(self)))
        for x in range(len(tp_coins)):
            block_temp=tp_coins[x]
            print("Block # "+str(x+1))
            for transaction in block_temp.verified_transaction:
                display_transaction(transaction)
                print('---------')

            print('=================')


class Block:

    tp_coins = []
    def __init__(self):
        self.verified_transaction=[]
        self.previous_block_hash=""
        self.Nonce=""
    
    



        


class Client:
    def __init__(self):
        random = Cryptodome.Random.new().read
        self._private_key = RSA.generate(2048, random)
        self._public_key = self._private_key.publickey()
        self._signer = PKCS1_v1_5.new(self._private_key)


    @property
    def identity(self):
        return binascii.hexlify(self._public_key.exportKey(format='DER')).decode('ascii')
    

class Transaction:
    def __init__(self, sender, recipient, value):
        self.sender = sender
        self.recipient = recipient
        self.value = value
        self.time = datetime.datetime.now()


    def to_dict(self):
        if self.sender == "Genesis":
            identity = "Genesis"
        else:
            identity = self.sender.identity

        return collections.OrderedDict({
                'sender': identity,
                'recipient': self.recipient,
                'value': self.value,
                'time' : self.time})
        
    def sign_transaction(self):
        private_key = self.sender._private_key
        signer = PKCS1_v1_5.new(private_key)
        h = SHA.new(str(self.to_dict()).encode('utf8'))
        return binascii.hexlify(signer.sign(h)).decode('ascii')
    


def display_transaction(transaction):
    dict = transaction.to_dict()
    print("sender : ",dict['sender'])
    print("-------")
    print("recipient : ",dict['recipient'])
    print("-------")
    print("value : ",dict['value'])
    print("-------")
    print("time : ",dict['time'])
    print("-------")
    



def mine(message, difficulty):
    assert difficulty >= 1
    prefix = '1'*difficulty
    for i in range(1000):
        digest = sha256((str(hash(message)) + str(i)).encode('utf-8')).hexdigest()
        if digest.startswith(prefix):
            print("after " + str(i) + " iterations found nonce: ", digest)
            return digest
        


if __name__ =='__main__':
    ayoub = Client()
    t0 = Transaction(
        "Genesis",
        ayoub.identity,
        500
    )

    block0 = Block()
    block0.previous_block_hash=None
    block0.Nonce=None
    block0.verified_transaction.append(t0)
    
    tp_coins.append(block0)

    #dump_blockchain(tp_coins)

    mine("test message",2)