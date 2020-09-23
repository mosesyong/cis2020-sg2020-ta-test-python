import logging
import json

from flask import request, jsonify, Response;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/optimizedportfolio', methods=['POST'])
def evaluatepf():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    listValue = data.get("inputs")
    result = {}
    result["outputs"] = [hedgeFunc(portfolioInput) for portfolioInput in listValue]        
    logging.info("My result :{}".format(result))
    return Response(json.dumps(result), mimetype='application/json')

def hedgeFunc(portfolioInput):
    portfolioName = portfolioInput["Portfolio"]["Name"]
    spotPriceVol = portfolioInput["Portfolio"]["SpotPrcVol"]
    portfolioValue = portfolioInput["Portfolio"]["Value"]
    
    indexFutures = portfolioInput["IndexFutures"]

    futures = []
    for future in indexFutures:
        futureName = future["Name"]
        futureCoeff = future["CoRelationCoefficient"]
        futureVol = future["FuturePrcVol"]
        futurePrice = future["IndexFuturePrice"]
        futureNotional = future["Notional"]

        optionalHedgeRatio = round(futureCoeff * (spotPriceVol/futureVol),3)
        numContract = round(optionalHedgeRatio * portfolioValue/(futurePrice*futureNotional))

        futures.append((futureName, optionalHedgeRatio, numContract, futureVol))

    hedge = sorted(futures, key = lambda x: (x[1], x[3], x[2]))[0]
    result =  {
        "HedgePostionName" : hedge[0],
        "OptimalHedgeRatio" : hedge[1],
        "NumFuturesContract" : hedge[2]
    }

    return result
    


        



    