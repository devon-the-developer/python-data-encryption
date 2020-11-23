import json
import encryptUpload

def changeUserInfo(data):
   
    name = data[0]
    age = data[1]
    uid = data[2]
    dbID = data[3]
    print(uid, "\nName : " + name, "\nAge: " + age)
    changeName = input("Do you want to change customer name? (y/n)")
    if (changeName == 'y'):
        newName = input("Change name to: ")
    else:
        newName = name
    changeAge = input("Do you want to change customer age? (y/n)")
    if (changeAge == 'y'):
        newAge = input("Change age to: ")
    else:
        newAge = age

    print("Updating to: " + newName + " " + newAge)
    #url = "https://crypto-ba4d.restdb.io/rest/contacts?q={UID" + f":{uid}".format(uid) + "}"
    #print(url)
    encryptUpload.run(True, {0: newName, 1: newAge, 2: uid, 3: dbID})

def run(data):
    print("Update: \n --------------")
    changeUserInfo(data)

