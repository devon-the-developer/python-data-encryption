import json
from base64 import b64decode, b64encode
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Hash import SHA256

import requests
key = b"Secret byte key "


def getFromDB(userID):
    #Request json where UID is userID
    url = "https://crypto-ba4d.restdb.io/rest/contacts" + '?q={"UID": ' + userID + "}"

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
        hashEn = b64decode(b64['Hash'])

        #set ciphermode and key to decrypt
        cipher = AES.new(key, AES.MODE_CBC, iv)
        name = decodePiece(nameEn, cipher)
        age = decodePiece(ageEn, cipher)
        hashPlain = decodePiece(hashEn, cipher)

        #Comments just to check its working
        print("\nDecrypted Response: \n-----------------")

        print("The name is: ", name)
        print("The age is: ", age)
        bData = bytes(name, 'utf-8') + bytes(age, 'utf-8')
    except (ValueError, KeyError):
        print("Incorrect Decryption")
    return (bData, hashPlain)

def run():
    userID = input("Enter the UserID: ")
    response = getFromDB(userID)
    responsejson = response.json()

    print("Database Response: ", responsejson)

    cusInfo = decrypt(responsejson)
    downloadedHash = cusInfo[1]
    ptHash = hash(cusInfo[0])
    print("Hash of Plaintext: ",ptHash)
    print("Downloaded Hash: ", downloadedHash)

    compareHashes(downloadedHash, ptHash)

def hash(byteText):
    hash_object = SHA256.new(data=byteText)
    return hash_object.hexdigest()

def compareHashes(databaseHash, textHash):
    if databaseHash == textHash:
        print("Hashes equal")
    else:
        print("Hashes not equal")