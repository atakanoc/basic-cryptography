import random, os, sys

# Substitution method
def sub_keygen():
    keyord = random.sample(range(65, 91), 26)      # Randomises alphabetic letter order but in numbers
    tempkey = [chr(l) for l in keyord]       # Converts numbers to characters
    key = ""
    for letter in tempkey:
        key += letter
    return key

def sub_encrypt(msg, k):     # Monoalphabetic method
    alphabet = [letter for letter in "abcdefghijklmnopqrstuvwxyz"]
    key = [letter for letter in k]
    try:
        keytable = {alphabet[i]:key[i] for i in range(26)}
    except IndexError:
        sys.exit("Invalid keysize, must have a length of 26")
    ciphertext = ""
    for letter in msg:
        if 65 <= ord(letter) <= 90:           # Makes sure to decapitalize letters
            templetter = chr(ord(letter) + 32)
            ciphertext += keytable.get(templetter)
        elif 97 <= ord(letter) <= 122:
            ciphertext += keytable.get(letter)
        else:
            ciphertext += letter     # non-letters don't get encrypted

    return ciphertext

def sub_decrypt(msg, k):
    alphabet = [letter for letter in "abcdefghijklmnopqrstuvwxyz"]
    key = [letter for letter in k]
    try:
        keytable = {key[i]:alphabet[i] for i in range(26)}
    except IndexError:
        sys.exit("Invalid keysize, must have a length of 26")
    print(keytable)
    plaintext = ""
    for letter in msg:
        if 65 <= ord(letter) <= 90:    # Key should already be capitalized
            plaintext += keytable.get(letter)
        elif 97 <= ord(letter) <= 122:    # In case it isn't capitalized
            templetter = chr(ord(letter) - 32)
            print(templetter, end="")
            print(keytable.get(templetter))
            plaintext += keytable.get(templetter)
        else:
            plaintext += letter

    return plaintext

# Transposition method
def trans_encrypt(msg, k):     # Rail fence method
    rowlist = []
    for i in range(int(k)):
        rowlist.append([])
    rowcount = 0
    for letter in msg:
        currow = rowlist[rowcount]
        currow.append(letter)

        if rowcount == int(k) - 1:
            down = False
        elif rowcount == 0:
            down = True

        if down == True:
            rowcount += 1
        else:
            rowcount -= 1

    finalstring = ""
    for row in rowlist:
        for letter in row:
            finalstring += letter

    return finalstring

def trans_decrypt(msg, k):
    # Calculations
    oglength = len(msg)


    # Create table
    rowlist = []
    for i in range(int(k)):
        rowlist.append([])
    for row in rowlist:
        for i in range(len(msg)):
            row.append([])

    # Fill table
    rowcount = 0
    columncount = 0
    for i in range(len(msg)):    # Deciding which blocks of the table will be written on

        currow = rowlist[rowcount]
        currow[columncount].append("-")

        # Row and column count
        columncount += 1

        if rowcount == int(k) - 1:
            down = False
        elif rowcount == 0:
            down = True

        if down == True:
            rowcount += 1
        else:
            rowcount -= 1

    # Filling blocks
    for row in rowlist:
        for block in row:
            if block == ["-"]:
                block[0] = msg[0]
                msg = msg[1:len(msg)]

    # Decode
    rowcount = 0
    columncount = 0
    plaintext = ""
    for i in range(oglength):  # Read table

        currow = rowlist[rowcount]
        block = currow[columncount]
        plaintext += block[0]

        # Row and column count
        columncount += 1

        if rowcount == int(k) - 1:
            down = False
        elif rowcount == 0:
            down = True

        if down == True:
            rowcount += 1
        else:
            rowcount -= 1

    return plaintext

# User interface
allowed = ["m", "r"]
x = ""
while x not in allowed:
    x = input("Monoalphabetic method or Rail Fence method? (m/r): ")

# Monoalphabetic
if x == "m":
    allowed = ["e", "d"]
    x = ""
    while x not in allowed:
        x = input("Would you like to encrypt or decrypt? (e/d): ")

    # Encrypt
    if x == "e":
        allowed = ["c", "g"]
        x = ""
        while x not in allowed:
            x = input("Would you like to input a custom key or generate one? (c/g): ")

        # Custom
        if x == "c":
            pathR = input("Enter plaintext file location: ")
            with open(pathR) as file:
                msg = file.read()
            k = input("Enter key: ")
            pathW = input("Path for encrypted file (include name of file): ")
            with open(pathW, "w") as file:
                file.write(sub_encrypt(msg, k))

        # Generate
        else:
            pathR = input("Enter plaintext file location: ")
            with open(pathR) as file:
                msg = file.read()
            k = sub_keygen()
            pathW = input("Path for encrypted file (include name of file): ")
            with open(pathW, "w") as file:
                ciphertext = "Ciphertext: " + sub_encrypt(msg, k) + "\nKey: " + k
                file.write(ciphertext)

    # Decrypt
    else:
        pathR = input("Enter Ciphertext file location: ")
        with open(pathR) as file:
            msg = file.read()
        pathW = input("Path for decrypted file (include name of file): ")
        k = input("Enter key: ")
        with open(pathW, "w") as file:
            file.write(sub_decrypt(msg, k))

# Rail Fence
else:
    allowed = ["e", "d"]
    x = ""
    while x not in allowed:
        x = input("Would you like to encrypt or decrypt? (e/d): ")

    # Encrypt
    if x == "e":
        pathR = input("Enter plaintext file location: ")
        pathW = input("Path for encrypted file (include name of file): ")
        k = input("Enter number of rows (key) (3-5 recommended): ")
        with open(pathR) as file:
            msg = file.read()
        with open(pathW, "w") as file:
            file.write(trans_encrypt(msg, k))

    # Decrypt
    else:
        pathR = input("Enter ciphertext file location: ")
        pathW = input("Path for decrypted file (include name of file): ")
        k = input("Enter number of rows (key): ")
        with open(pathR) as file:
            msg = file.read()
        with open(pathW, "w") as file:
            file.write(trans_decrypt(msg, k))

print("Done.")