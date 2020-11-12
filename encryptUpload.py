import json
from base64 import b64encode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes

import requests
from Crypto import Random


def encryptPiece(inputVar, cipher):
    # pass in data to encrypt and the cipher set with key
    data = inputVar
    ct_bytes = cipher.encrypt(pad(data, AES.block_size))
    return ct_bytes


def aesEncrypt(name, age, hash):
    # variables must be in bytes - b"-"
    name = name
    age = age
    hash = bytes(hash, 'utf-8')
    print("compare", type(name), type(age), type(hash))
    key = b"Secret byte key "  # 16 bytes long

    # set cipher to use and encrypt individual data
    cipher = AES.new(key, AES.MODE_CBC)
    ne_bytes = encryptPiece(name, cipher)
    ae_bytes = encryptPiece(age, cipher)
    hash_bytes = encryptPiece(hash, cipher)
    iv = b64encode(cipher.iv).decode()


    # encoded data is returned in format that can be sent in JSON
    nameEn = b64encode(ne_bytes).decode()
    ageEn = b64encode(ae_bytes).decode()
    hashEn = b64encode(hash_bytes).decode()
    print("String of encoded hash", hashEn)
    print("result: ", nameEn, ageEn, iv, hashEn)
    return (nameEn, ageEn, iv, hashEn)


def sendToDB(data):
    url = "https://crypto-ba4d.restdb.io/rest/contacts"

    payload = json.dumps({"Name": data[0], "Age": data[1], "iv": data[2], "Hash": data[3]})
    headers = {
        'content-type': "application/json",
        'x-apikey': "a738e377f1dbb542fc42441da180a476685f6",
        'cache-control': "no-cache"
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    print(response)


def run():
    cusName = input("What is the name of the customer? ")
    cusAge = input("What is their age? ")
    # join name and age together as strings
    hashingString = cusName + cusAge
    # Convert strings into bytes
    cusName = bytes(cusName, 'utf-8')
    cusAge = bytes(cusAge, 'utf-8')

    # convert to bytes
    bHashString = bytes(hashingString, 'utf-8')
    print("String to be hashed in bytes",bHashString)

    # hash the result
    hashOfStrings = hash(bHashString)
    print("Result of hashing byte string", hashOfStrings)
    # send that hash to be encoded

    # hashing plain text
    ptHash = hash(cusName + cusAge)
    print("hash before encoding.. ", ptHash)


    # Encrypt given data
    encryptMsg = aesEncrypt(cusName, cusAge, hashOfStrings)

    # Send Encrypted data to DB
    sendToDB(encryptMsg)


def hash(plainText):
    hash_object = SHA256.new(data=plainText)
    print("hexdigest",hash_object.hexdigest())
    print("digest",hash_object.digest())
    return hash_object.hexdigest()

