import logging
import json

from flask import request, jsonify, Response;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/intelligent-farming', methods=['POST'])
def evaluateIf2():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    listValue = data.get("list");
    for value in listValue:
        newValue = reorderSequence(value.get("geneSequence"))
        value["geneSequence"] = newValue
    logging.info("My result :{}".format(data))
    return Response(json.dumps(data), mimetype='application/json');



def reorderSequence(sequence):
    pointMap = {}
    pointMap["AAA"] = -20
    pointMap["ACGT"] = 15
    pointMap["CC"] = 25

    countA = 0
    countC = 0
    countG = 0
    countT = 0

    for letter in sequence:
        if letter == "A":
            countA +=1
        elif letter == "C":
            countC +=1
        elif letter == "G":
            countG +=1
        elif letter == "T":
            countT +=1
        else:
            print("Error, unknown letter " + letter)

    # print(countA, countC, countG, countT)
    newSequence = ""

    while(countC > 2):
        newSequence += "CC"
        countC -= 2

    while(countA > 0 and countC > 0 and countG > 0 and countT > 0):
        newSequence += "ACGT"
        countA -= 1
        countC -= 1
        countG -= 1
        countT -= 1

    while(countA > 2 and countC > 0):
        newSequence += "AAC"
        countA -= 2
        countC -= 1

    while(countA > 2 and countG > 0):
        newSequence += "AAG"
        countA -= 2
        countG -= 1

    while(countA > 2 and countT >0):
        newSequence += "AAT"
        countA -= 2
        countT -= 1

    while(countG > 0):
        newSequence += "G"
        countG -= 1

    while(countT > 0):
        newSequence += "T"
        countT -= 1

    while(countA > 0):
        newSequence += "A"
        countA -= 1
    return newSequence

