import json
import requests

from base64 import b64encode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes

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
    return (nameEn, ageEn, iv, hashEn)


def sendToDB(data, url, updateCus):
    #url = "https://crypto-ba4d.restdb.io/rest/contacts"

    payload = json.dumps({"Name": data[0], "Age": data[1], "iv": data[2], "Hash": data[3]})
    headers = {
        'content-type': "application/json",
        'x-apikey': "a738e377f1dbb542fc42441da180a476685f6",
        'cache-control': "no-cache"
    }

    if(updateCus == True):
        restType = "PUT"
    else: 
        restType = "POST"

    print(restType)
    response = requests.request(restType, url, data=payload, headers=headers)
    print(response)    


def run(updateCus, info):

    if (updateCus == True):
        cusName = info[0]
        cusAge = info[1]
        cusUID = info[2]
        dbID = info[3]
        print(cusName, cusAge, cusUID)
        url = "https://crypto-ba4d.restdb.io/rest/contacts/" + dbID
        print(url)
    else:
        cusName = input("What is the name of the customer? ")
        cusAge = input("What is their age? ")
        url = "https://crypto-ba4d.restdb.io/rest/contacts"


    # join variables together to be hashed later
    strOfData = cusName + cusAge
    # Convert strings into bytes
    cusName = bytes(cusName, 'utf-8')
    cusAge = bytes(cusAge, 'utf-8')

    # convert to bytes
    bHashString = bytes(strOfData, 'utf-8')
    print("String to be hashed in bytes",bHashString)

    # hash the result
    hashOfStrings = hash(bHashString)
    print("Result of hashing byte string", hashOfStrings)

    # Encrypt given data
    encryptMsg = aesEncrypt(cusName, cusAge, hashOfStrings)

    # Send Encrypted data to DB
    print(encryptMsg, url, updateCus)
    sendToDB(encryptMsg, url, updateCus)


def hash(plainText):
    hash_object = SHA256.new(data=plainText)
    print("hexdigest",hash_object.hexdigest())
    return hash_object.hexdigest()

