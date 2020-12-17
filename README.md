# python-data-encryption
CLI Data encryption script to encrypt data for storage on a db and decryption on client end
Was developed by devon-the-developer & Micahgard for an assignment.

Python script to allowed the encryption of a "customers" data for storage on a external database. 

Using Python 3 
Database use at restdb.io
Using the cryptographic library of pycryptdome

# How it works 

Download and run in command line by using the command: 

```python3 clientScript.py```

Gives user options to either upload data or download and then change if wanted.

Uploading:

When uploading the plaintext is hashed and then encrypted.
The hash of the plaintext is then encrypted.
All of this encrypted data is then uploaded to the database via REST Protocols

Downloading:

When downloading, all the data is decrypted with appropriate method and key.
The plaintext of the downloaded is then hashed and compared with the hash from the database to check for integrity.
The option is then given to the user to change the data stored for that customer.

Whilst the API Key to restdb is available in code, that has been done to allow for proper marking of the project. We'll look to remove this in future adjustments to the code.

# Libraries

    pycryptodome
    requests
    json
    base64
