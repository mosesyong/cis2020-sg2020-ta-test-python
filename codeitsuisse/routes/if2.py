import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/intelligent-farming-2', methods=['GET'])
def evaluateIf2():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    logging.info("My result :{}".format(data))
    return json.dumps(data);



