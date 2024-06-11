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

    MAX_BLOCK_SIZE=1500

    def __init__(self):
        self.verified_transaction=[]
        self.previous_block_hash=""
        self.Nonce=""

    def get_size_block(self):
        size = 0
        for transaction in self.verified_transaction:
            size+= len(json.dumps(transaction.to_dict()))
        return size

    def can_add_transaction(self, transaction):
        current_size = self.get_size_block()
        transaction_size = len(json.dumps(transaction.to_dict()))
        if (current_size + transaction_size) > self.MAX_BLOCK_SIZE:
            return False
        return True

    
    

class Client:
    def __init__(self,balance=0):
        random = Cryptodome.Random.new().read  #creation random byte
        self._private_key = RSA.generate(1024, random)  #private key = rsa de 2048 bites a partir de random  (2048 est le longuer minimum)
        self._public_key = self._private_key.publickey()  #creattion de cle public a partir du cle prive
        self._signer = PKCS1_v1_5.new(self._private_key) #signer le cle prive
        self._balance = balance


    @property
    def identity(self):
        return binascii.hexlify(self._public_key.exportKey(format='DER')).decode('ascii')#identite de client a partir de cle public
    

class Transaction:
    def __init__(self, sender, recipient, value):
        self.sender = sender
        self.recipient = recipient
        self.value = value
        self.time = datetime.datetime.now()
        self.signature = self.sign_transaction()

    def to_dict(self):
        if self.sender == "Genesis":
            identity = "Genesis"
        else:
            identity = self.sender.identity

        return collections.OrderedDict({
                'sender': identity,
                'recipient': self.recipient.identity,
                'value': self.value,
                'time' : self.time.isoformat()})

    def sign_transaction(self):
        private_key = self.sender._private_key
        signer = PKCS1_v1_5.new(private_key)
        h = SHA.new(str(self.to_dict()).encode('utf8'))
        return binascii.hexlify(signer.sign(h)).decode('ascii')
    


def display_transaction(transaction): #affichae des informations de transaction
    dict = transaction.to_dict()
    print("sender : ",dict['sender'])
    print("-------")
    print("recipient : ",dict['recipient'])
    print("-------")
    print("value : ",dict['value'])
    print("-------")
    print("time : ",dict['time'])
    print("-------")
    



def mine(message, difficulty):#creation of sha256 for a message that follows the"11xxxxxxxxx" format, the number of 1's is determined by the difficutly(1*difficulty)
    assert difficulty >= 1
    prefix = '1'*difficulty
    for i in range(1000):
        digest = sha256((str(hash(message)) + str(i)).encode('utf-8')).hexdigest()
        if digest.startswith(prefix):
            #print("after " + str(i) + " iterations found nonce: ", digest)
            return digest
        

def verify_signature(transaction):
    public_key = transaction.sender._public_key
    signer = PKCS1_v1_5.new(public_key)
    h = SHA.new(str(transaction.to_dict()).encode('utf8'))
    return signer.verify(h, binascii.unhexlify(transaction.signature))


def check_balance(transaction):
    value = transaction.value
    sender_balance = transaction.sender._balance

    if(value <= sender_balance):
        return True
    return False

def execute_transaction(transaction):
    sender = transaction.sender
    recipient = transaction.recipient
    value = transaction.value

    sender._balance -= value
    recipient._balance += value
    



if __name__ =='__main__':
    

    Dinesh = Client(900)
    Ramesh = Client(800)
    Seema = Client(300)
    Vijay = Client(500)

    transactions = [
    Transaction(Dinesh, Ramesh, 15.0),
    Transaction(Dinesh, Seema, 20.0),
    Transaction(Dinesh, Vijay, 25.0),
    Transaction(Ramesh, Dinesh, 30.0),
    Transaction(Ramesh, Seema, 35.0),
    Transaction(Ramesh, Vijay, 40.0),
    Transaction(Seema, Dinesh, 45.0),
    Transaction(Seema, Ramesh, 50.0),
    Transaction(Seema, Vijay, 55.0),
    Transaction(Vijay, Dinesh, 60.0),
    Transaction(Vijay, Ramesh, 65.0),
    Transaction(Vijay, Seema, 70.0)
]
#    for i in range(len(transactions)):
#        print("size transaction #1 :",len(json.dumps(transactions[i].to_dict())))

    block = Block()
    while(block.can_add_transaction(transactions[LAST_TRANSACTION_INDEX]) and LAST_TRANSACTION_INDEX<len(transactions)):
        temp_transaction = transactions[LAST_TRANSACTION_INDEX]
        print("transaction #",LAST_TRANSACTION_INDEX)
        b1 = True
        try:
            verify_signature(temp_transaction)
            print("signature verified")
        except(ValueError,TypeError):
            b1 = False
            print("wrong signature")
        
        if b1 and check_balance(temp_transaction):
            block.verified_transaction.append(temp_transaction)
            execute_transaction(temp_transaction)
        else:
            print("non validated")
        

        LAST_TRANSACTION_INDEX +=1
        if(LAST_TRANSACTION_INDEX<len(transactions)):
            if block.can_add_transaction(transactions[LAST_TRANSACTION_INDEX])==False:

                block.previous_block_hash = LAST_BLOCK_HASH
                block.Nonce = mine(block, 2)
                digest = hash(block)
                tp_coins.append(block)
                LAST_BLOCK_HASH = digest

                block = Block()
                print("new block added")
            else:
                print("wroking on the same block")
        else:
            break
    tp_coins.append(block)

    dump_blockchain(tp_coins)
