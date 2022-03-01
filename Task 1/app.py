from flask import Flask, request, jsonify , render_template , send_from_directory 
from PIL import Image 
import numpy as np
import math
import ccv
import base64
from io import BytesIO
import os
import time
import match
app = Flask(__name__)



A_directions =  {"direction": "F"}
M_directions = {"direction" : "L"}
mode = {"mode" : False}
angle ={"angle" : 3}
rfid = {"rfid" : "xxxx"}



@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r
    
@app.route('/')
def hello_world():

    # new_frame_name = "frame" + str(time.time()) + ".jpg"
    # for filename in os.listdir('static/'):
    #     if filename.startswith('frame'):  # not to remove other images
    #          os.remove('static/' + filename)
    # res = Image.open('static/ress.jpg')
    # res.save('static/' + new_frame_name)
    return  render_template('render.html' , frame='ress.jpg')
    # return "Welcome"

@app.route("/frame", methods=["POST"])
def process_image():
    # file = request.files['image']
    # # os.path.join is used so that paths work in every operating system
    # file.save(os.path.join(file.filename))

    # with open(file.filename) as f:
    #     file_content = f.read()
    req_data= request.get_json(force=True)
    # data.append(req_data['data']['base64'])
    # f = open(file.stream, 'r')
    # data = f.read()
    # f.closed
    # im = Image.open(BytesIO(base64.b64decode(req_data['data']['base64'])))
    im = Image.open(BytesIO(base64.b64decode(req_data["data"]["base64"])))
    # converting PIL image to opencv image
    # width, height = im.size
    # print(width, height)
    f = np.array(im)
    f = f[:, :, ::-1].copy()
    # im.save('immm.png', 'PNG')

    # with open("im.jpg", "wb") as fh:
    #     fh.write(data.decode('base64'))

    # file.save('im.jpg')
    y = match.object(f)
    x= ccv.get_angle(f)
    angle.update({"angle":x})
    # Read the image via file.stream
    # img = Image.open(file.stream)
    if x > 120 :
        if y == "left" :
            A_directions.update({"direction": "R"})
        elif y ==" right":
            A_directions.update({"direction": "L"})
        else : 
            A_directions.update({"direction": "R"})



    elif x < 52 : 
        if y == "right" : 
            A_directions.update({"direction": "L"}) 
        elif  y == "left":
            A_directions.update({"direction": "R"}) 
        else : 
            A_directions.update({"direction": "L"}) 


    else : 
        if y == "left" : 
            A_directions.update({"direction": "R"}) 
        elif y == "right" : 
            A_directions.update({"direction": "L"}) 
        else : 
            A_directions.update({"direction": "F"}) 


    # if x > 120 :
    #         A_directions.update({"direction": "R"})



    # elif x < 46 : 
    #         A_directions.update({"direction": "L"}) 

    # elif x == -90 : 
    #     A_directions.update({"direction": "B"})
    # else : 
    #     A_directions.update({"direction": "F"}) 

        
    return jsonify({'msg': 'success'})

@app.route('/directions', methods=['GET'])
def get_directions():
    if mode["mode"] == True:
        all_data = {"direction" : A_directions["direction"], "mode" : mode["mode"]}
        return jsonify(all_data)
    if mode["mode"]== False :
         all_data = {"direction" : M_directions["direction"], "mode" : mode["mode"]}
         return jsonify(all_data)


@app.route('/change_mode', methods=['POST'])
def post_mode():
    req_data= request.get_json(force=True)
    mode.update({"mode": req_data["mode"]})
    return jsonify({'msg': 'success'})



@app.route('/mode', methods=['GET'])
def get_mode():
    return jsonify(mode)
@app.route('/angle', methods=['GET'])
def get_angle():
    return jsonify(angle)

@app.route('/directions', methods=['POST'])
def post_m_directions():
    req_data= request.get_json(force=True)
    M_directions.update({"direction": req_data["direction"]})
    return jsonify({'msg': 'success'})

@app.route('/rfid', methods=['POST'])
def post_rfid():
    req_data= request.get_json(force=True)
    rfid.update({"rfid": req_data["rfid"]})
    return jsonify({'msg': 'success'})

@app.route('/rfid', methods=['GET'])
def get_rfid():
    return jsonify(rfid)



if __name__ == "__main__":
    app.run(debug=True, host="172.28.134.58")