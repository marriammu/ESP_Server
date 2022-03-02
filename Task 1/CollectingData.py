
from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np
import openpyxl
import pickle
WifiReadings=[]
app = Flask(__name__)
CORS(app)
model = pickle.load(open('model.pkl','rb'))
@app.route('/Readings', methods=['POST'])
def Data():
    WifiReadings.clear()
    request_data = request.get_json()
    WifiReadings.append(request_data['STUDBME2'])
    WifiReadings.append(request_data['Aalaa Tarek'])
    WifiReadings.append(request_data['Amira'])
    WifiReadings.append(request_data['Esraa'])
    WifiReadings.append(request_data['STUDBME1'])
    WifiReadings.append(request_data['Sbme-Staff'])
    WifiReadings.append(request_data['RehabLab'])
    WifiReadings.append(request_data['CMP_LAB1'])
    WifiReadings.append(request_data['CMP_LAB3'])
    WifiReadings.append(request_data['Gadgooda'])
    # WifiReadings.append(request_data['iPhone 11'])
    NpWifiReadings=np.array(WifiReadings)
    print(NpWifiReadings)
    prediction = model.predict([NpWifiReadings])
    global output 
    output = np.int(prediction[0])
    
    print(type(1))
     
    return jsonify(WifiReadings)

@app.route('/Readings', methods=['GET'])
def GetData():
 
    label = {"label": output}    
    print(label)

    return (jsonify(label))

if __name__ == "__main__":
    app.run(host="IP Address", port=80, debug=True)