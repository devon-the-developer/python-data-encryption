import encryptUpload
import decryptDownload

def runOption():

    #Get User Input and run associated script
    loadscript = input("Would you like to upload or download? (u/d) ")
    loadscript.casefold()

    if (loadscript == 'u'):
        encryptUpload.run()
    elif(loadscript == 'd'):
        decryptDownload.run()
    else:
        print("Not a valid option")
        runOption()

print ("Welcome to the Terminal! \n")
runOption()


