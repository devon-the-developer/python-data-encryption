import json
from base64 import b64decode, b64encode
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Hash import SHA256

import requests
import update
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
    except (ValueError, KeyError):
        print("Incorrect Decryption")
    return (name, age, hashPlain)

def run():
    userID = input("Enter the UserID: ")
    response = getFromDB(userID)
    responsejson = response.json()

    print("Database Response: ", responsejson)

    cusInfo = decrypt(responsejson)
    cusUID = responsejson[0]['UID']
    cusName = cusInfo[0]
    cusAge = cusInfo[1]
    downloadedHash = cusInfo[2]
    ptHash = hash(bytes(cusName, 'utf-8') + bytes(cusAge, 'utf-8'))
    print("Hash of Plaintext: ",ptHash)
    print("Downloaded Hash: ", downloadedHash)

    compareHashes(downloadedHash, ptHash)
    updateInfo(cusName, cusAge, cusUID)

def hash(byteText):
    hash_object = SHA256.new(data=byteText)
    return hash_object.hexdigest()

def compareHashes(databaseHash, textHash):
    if databaseHash == textHash:
        print("Hashes equal")
    else:
        print("Hashes not equal")

def updateInfo (cusName, cusAge, cusUID):
    print("CusInfo: ", cusName + " " + cusAge)
    
    updateQ = input("Would you like to update user info? (y/n)")
    if (updateQ == "y"):
        update.run({0: cusName, 1: cusAge, 2: cusUID})
    elif (updateQ == "n"):
        print("Ending program")
    else:
        print("That is not a valid response.")
        updateInfo(cusName, cusAge, cusUID)