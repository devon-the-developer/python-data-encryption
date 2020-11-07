import json
from base64 import b64encode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

import requests
from Crypto import Random

def encryptPiece(inputVar, cipher):
    #pass in data to encrypt and the cipher set with key
    data = inputVar
    ct_bytes = cipher.encrypt(pad(data, AES.block_size))
    return ct_bytes

def aesEncrypt(name, age):
    #variables must be in bytes - b"-"
    name = name
    age = age
    key = b"Secret byte key " #16 bytes long

    #set cipher to use and encrypt individual data
    cipher = AES.new(key, AES.MODE_CBC)
    ne_bytes = encryptPiece(name, cipher)
    ae_bytes = encryptPiece(age, cipher)
    iv = b64encode(cipher.iv).decode()

    #encoded data is returned in format that can be sent in JSON
    nameEn = b64encode(ne_bytes).decode()
    ageEn = b64encode(ae_bytes).decode()
    print("result: ",  nameEn, ageEn, iv)
    return (nameEn, ageEn, iv)

def sendToDB(data): 
    url = "https://crypto-ba4d.restdb.io/rest/contacts"

    payload = json.dumps( {"Name": data[0],"Age": data[1], "iv": data[2]} )
    headers = {
    'content-type': "application/json",
    'x-apikey': "a738e377f1dbb542fc42441da180a476685f6",
    'cache-control': "no-cache"
    }

    response = requests.request("POST", url, data=payload, headers=headers) 
    print(response)

def run():
    #Encrypt given data
    encryptmsg = aesEncrypt(b"Nathaniel", b"70")

    #Send Encrypted data to DB
    sendToDB(encryptmsg)









