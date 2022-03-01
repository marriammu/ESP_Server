
from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np
import openpyxl
import pickle
WifiReadings=[]
app = Flask(__name__)
CORS(app)

@app.route('/Readings', methods=['POST'])
def Data():
    request_data = request.get_json()
    WifiReadings.append(request_data['strength'])
    WifiReadings.append(request_data['data'])
    print(jsonify(WifiReadings))    
    return jsonify(WifiReadings)

@app.route('/Readings', methods=['GET'])
def GetData():
    label = {"label":10}    
    print(label)
    return jsonify(label)

if __name__ == "__main__":
    app.run(host="192.168.1.3", port=80, debug=True)