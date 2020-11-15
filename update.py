def updateUserInfo(uid, userInfo):
    print(uid, " :  ", userInfo)
    url = "https://crypto-ba4d.restdb.io/rest/contacts?q={UID" + f":{uid}".format(uid) + "}"
    print(url)

    #payload = json.dumps({"Name": data[0], "Age": data[1], "iv": data[2], "Hash": data[3]})
    #headers = {
        #'content-type': "application/json",
        #'x-apikey': "a738e377f1dbb542fc42441da180a476685f6",
        #'cache-control': "no-cache"
    #}

    #response = requests.request("PUT", url, data=payload, headers=headers)
    #print(response)

def run():
    print("Update")
    updateUserInfo(4, "somehing here")
