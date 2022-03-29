from flask import Flask, jsonify
from flask_cors import CORS
from LaneDetection import *

app = Flask(__name__)
CORS(app)
# for blue color

low=np.array([60,40,40])
high=np.array([150,255,255])
@app.route('/')
def main():
    return "main Page"

@app.route('/DetectAngle', methods=['GET'])
def process():
    image=plt.imread('lane 2.jpg')
    # image=GetImageFromMobile()
    laneLines =LaneDetection(image, low, high)
    laneLinesImage = LinesDisplaying(image, laneLines)
    steeringAngle= SteeringAngle(image, laneLines)
    currentAngle = steeringAngle
    finalImage = displayHeadingLine(laneLinesImage, currentAngle)

    resultJSON = {"angle": currentAngle}
    print(resultJSON)
    return jsonify(resultJSON)


if __name__ == '__main__':
    app.run(host='',port=3000,debug=True)

