
from flask import Flask, jsonify, request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
@app.route('/rectangle', methods=['POST'])
def rectangle():
    global rectangle_id
    rectangle_id=0
    print (rectangle_id)
    return ('Rectangle')

@app.route('/triangle', methods=['POST'])
def triangle():
    global triangle_id
    triangle_id=1
    print (triangle_id)
    return ('Triangle')

@app.route('/square', methods=['POST'])
def square():
    global square_id
    square_id=2
    print (square_id)
    return ('Square')

if __name__ == "__main__":
    app.run(host="192.168.1.210", port=4000, debug=True)