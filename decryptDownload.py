import json
from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

import requests
key = b"Secret byte key "


def getFromDB():
    url = "https://crypto-ba4d.restdb.io/rest/contacts"

    headers = {
    'content-type': "application/json",
    'x-apikey': "a738e377f1dbb542fc42441da180a476685f6",
    'cache-control': "no-cache"
    }

    response = requests.request("GET", url, headers=headers)
    return response

def decodePiece(inputVar, cipher):
    plaintext = unpad(cipher.decrypt(inputVar), AES.block_size).decode()
    return plaintext

def decrypt(jsondata):
    try:
        #get json from DB and then grab each encrypted variable
        item = jsondata
        b64 = item[-1]
        iv = b64decode(b64['iv'])
        nameEn = b64decode(b64['Name'])
        ageEn = b64decode(b64['Age'])

        #set ciphermode and key to decrypt
        cipher = AES.new(key, AES.MODE_CBC, iv)
        name = decodePiece(nameEn, cipher)
        age = decodePiece(ageEn, cipher)

        #Comments just to check its working
        print("The name is: ", name)
        print("The age is: ", age)
    except (ValueError, KeyError):
        print("Incorrect Decryption")

def run():
    response = getFromDB()
    responsejson = response.json()

    print("______: ", responsejson[-1])

    decrypt(responsejson)