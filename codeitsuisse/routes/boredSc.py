import logging
import json
import string
import numpy as np

from flask import request, jsonify, Response

from codeitsuisse import app;

logger = logging.getLogger(__name__)
alphabet = string.ascii_lowercase # "abcdefghijklmnopqrstuvwxyz"
wordSet = set(line.strip() for line in open('./codeitsuisse/routes/en.txt'))

@app.route('/bored-scribe', methods=['POST'])
def evaluateBoredScribe():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    for jsonObject in data:
        encryptedText = jsonObject["encryptedText"]
        selectedText = ""
        lowestEntropy = 10000
        for i in range(0,26):
            decryptedText = unCaesar(encryptedText,i)
            entropy = getEntropy(decryptedText)
            if entropy < lowestEntropy:
                selectedText = decryptedText
                lowestEntropy = entropy
        # print(addSpace(selectedText))
        del jsonObject["encryptedText"]
        jsonObject["encryptionCount"] = 1
        jsonObject["originalText"] = ' '.join(addSpace(selectedText))
    logging.info("data sent for evaluation {}".format(data))
    return Response(json.dumps(data), mimetype='application/json');

def unCaesar(encrypted_message, key):
    
    decrypted_message = ""
    for c in encrypted_message:

        if c in alphabet:
            position = alphabet.find(c)
            new_position = (position - key + 26) % 26
            new_character = alphabet[new_position]
            decrypted_message += new_character
        else:
            decrypted_message += c

    return(decrypted_message)

#test

def addSpace(decryptedText):
    output = []
    while(len(decryptedText) > 0):
        hasWord = False
        for i in range(len(decryptedText), -1, -1):
            splicedWord = decryptedText[0:i]
            if splicedWord in wordSet:            
                output.append(splicedWord)
                decryptedText = decryptedText[i:]
                hasWord = True
            if hasWord:
                break
        if hasWord == False:
            output.append(decryptedText)
            decryptedText = ""
        
    return output
    
def getEntropy(inputString):
    ENGLISH_FREQS = [0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015, 0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406,0.06749, 0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758, 0.00978, 0.02360, 0.00150, 0.01974, 0.00074]

    sumOfEntropy = 0
    for i in range(len(inputString)):
        ch = inputString[i]
        chInt = ord(ch)
        if chInt >=97 and chInt <= 122:
            sumOfEntropy += np.log(ENGLISH_FREQS[chInt-97])
    return (sumOfEntropy * -1)/ np.log(2.0)/ len(inputString)

