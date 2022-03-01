from asyncore import write
from cProfile import label
from itertools import count
import json
import os
from flask import Flask, jsonify, request , make_response
from flask_cors import CORS
import pandas as pd
import openpyxl

app = Flask(__name__)
CORS(app)

@app.route('/Readings', methods=["POST"])
def Data():
    count = 0
    request_data = request.get_json()
    data = [] 
    names=[]
    labels=[]
    data.append(request_data['strength'])
    names.append(request_data['name'])
    labels.append(request_data['label'])
    print(data)
    df_data = pd.DataFrame(labels, columns=['label'])
    df_data['name']=names
    df_data['strength']=data
    path = os.getcwd()
    filename = 'data.xlsx'
    sheet_name = "3201"
    if (os.path.exists(filename)) :
        wb = openpyxl.load_workbook(filename)
        if(not (sheet_name in wb.sheetnames)):
            wb.create_sheet(sheet_name)
        ws = wb.active
        row=ws.max_row
        ws.cell(column=1, row=row+1,value=labels[0])
        ws.cell(column=2, row=row+1,value=names[0])
        ws.cell(column=3, row=row+1, value=data[0])
        count=count+1
        wb.save(filename)
    else:
        df_data.to_excel(filename, index=False, sheet_name=sheet_name)
    
    return jsonify(data1)
@app.route('/Readings', methods=['GET'])
def GetData():
    data1 = {"data":10}    
    print(data1)
    return jsonify(data1)

if __name__ == "__main__":
    app.run(host="172.28.130.32", port=80, debug=True)