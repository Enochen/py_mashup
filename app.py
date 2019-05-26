
#Authors: Austin George, Enoch Chen
#Purpose: Allows for the functionality for Half-Bot-Half-Brain

import mash
from flask import Flask, render_template, request
from flask import jsonify
from flask_cors import CORS, cross_origin


app = Flask(__name__)
app.config["DEBUG"] = True
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resources={r"/api/mash": {"origins": "http://localhost:3000"}})

@app.route('/',methods=['GET'])
def index():
    return render_template("main_page.html")

@app.route('/api/mash', methods=['POST'])
def madlibs():
    o = request.get_json(force=True)['original']
    m = request.get_json(force=True)['modifier']
    res = mash.mashup(original=o, modifier=m)
    return jsonify(original=res[0], modifier=res[1], result=res[2])
    
if __name__ == '__main__':
    app.run()