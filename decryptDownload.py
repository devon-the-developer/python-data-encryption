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
    print("decode piece", inputVar, cipher)
    plaintext = unpad(cipher.decrypt(inputVar), AES.block_size).decode()
    print("plaint text after being decoded", plaintext)
    print("_________________________")
    return plaintext

def decrypt(jsondata):
    try:
        #get json from DB and then grab each encrypted variable
        item = jsondata
        b64 = item[-1]
        iv = b64decode(b64['iv'])
        nameEn = b64decode(b64['Name'])
        ageEn = b64decode(b64['Age'])
        print("encoded age.. ", type(ageEn))
        hashEn = b64decode(b64['Hash'])
        print("Encoded hash...", type(hashEn))


        #set ciphermode and key to decrypt
        cipher = AES.new(key, AES.MODE_CBC, iv)
        name = decodePiece(nameEn, cipher)
        age = decodePiece(ageEn, cipher)
        print("Decoded age...", type(age))
        hashPlain = decodePiece(hashEn, cipher)
        print("decoded hash...", type(hashPlain))

        #Comments just to check its working
        print("\nDecrypted Response: \n-----------------")

        print("The name is: ", name)
        print("The age is: ", age)
        #print("The hash is: ", hashPlain)
    except (ValueError, KeyError):
        print("Incorrect Decryption")
    return (bytes(name, 'utf-8') + bytes(age, 'utf-8'), hashPlain)

def run():
    userID = input("Enter the UserID: ")
    response = getFromDB(userID)
    responsejson = response.json()

    print("Encrypted Response: ", responsejson[-1])

    returnedObject = decrypt(responsejson)
    print(type(returnedObject))
    ptHash = hash(returnedObject[0])
    print("2",ptHash)
    print("3", returnedObject[1])
    #compareHashes(, ptHash)

def hash(byteText):
    #print(type(byteText))
    hash_object = SHA256.new(data=byteText)
    #hashEn = b64encode(hash_object).decode()
    #print(hashEn)
    #print(hash_object.hexdigest())
    #print(hash_object.digest())
    return hash_object.hexdigest()

def compareHashes(databaseHash, textHash):
    if databaseHash == textHash:
        print("Hashes equal")
    else:
        print("Hashes not equal")