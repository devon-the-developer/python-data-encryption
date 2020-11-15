import json

def changeUserInfo(data):
    name = data[0]
    age = data[1]
    uid = data[2]
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
    url = "https://crypto-ba4d.restdb.io/rest/contacts?q={UID" + f":{uid}".format(uid) + "}"
    print(url)

    #payload = json.dumps({"Name": "data[0]", "Age": data[1], "iv": data[2], "Hash": data[3]})
    #headers = {
        #'content-type': "application/json",
        #'x-apikey': "a738e377f1dbb542fc42441da180a476685f6",
        #'cache-control': "no-cache"
    #}

    #response = requests.request("PUT", url, data=payload, headers=headers)
    #print(response)

def run(data):
    print("Update: \n --------------")
    changeUserInfo(data)

