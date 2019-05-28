
#Authors: Austin George, Enoch Chen
#Purpose: Allows for the functionality for Half-Bot-Half-Brain

import mash
from flask import Flask, render_template, request
from flask import jsonify
from flask_cors import CORS, cross_origin


app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resources={r"/api/mash": {"origins": "*"},r"/api/wiki": {"origins": "*"}})

@app.route('/',methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/api/wiki', methods=['POST'])
def wiki():
    return jsonify(result=mash.random_wiki())

@app.route('/api/mash', methods=['POST'])
def madlibs():
    o = request.get_json(force=True)['original']
    m = request.get_json(force=True)['modifier']
    c = request.get_json(force=True)['craziness']
    res = mash.mashup(original=o, modifier=m, craziness=c)
    return jsonify(original=res[0], modifier=res[1], result=res[2])
    
if __name__ == '__main__':
    app.run()