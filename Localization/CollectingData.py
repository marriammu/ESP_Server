
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
    print(request_data)
    WifiReadings.append(request_data['STUDBME2'])
    WifiReadings.append(request_data['Aalaa Tarek'])
    WifiReadings.append(request_data['khaleesiH'])
    WifiReadings.append(request_data['Esraa'])
    WifiReadings.append(request_data['STUDBME1'])
    WifiReadings.append(request_data['Sbme-Staff'])
    WifiReadings.append(request_data['RehabLab'])
    WifiReadings.append(request_data['CMP_LAB1'])
    WifiReadings.append(request_data['CMP_LAB3'])
    WifiReadings.append(request_data['Gadgooda'])
    prediction = model.predict([WifiReadings])
    global output
    output = int(prediction[0])
    print("label")
    print(output)
    # WifiReadings.append(request_data['iPhone 11'])
    # global NpWifiReadings
    # NpWifiReadings=np.array(WifiReadings)
    # print(NpWifiReadings)     
    return jsonify(WifiReadings)
# if(len(WifiReadings)!=0):
    

@app.route('/Readings', methods=['GET'])
def GetData():
 
    label = {"label": output}    
    # print(label)
    return (jsonify(label))

if __name__ == "__main__":
    app.run(host="192.168.1.6", port=80, debug=True)