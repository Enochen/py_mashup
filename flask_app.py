
#Authors: Austin George, Enoch Chen
#Purpose: Allows for the functionality for Half-Bot-Half-Brain

import mash
from flask import Flask, render_template
from flask import jsonify


app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/',methods=['GET'])
def index():
    return render_template("main_page.html")

#Receives One Story
@app.route('/api/mash', methods=['POST'])
def mash():
    o = request.json['original']
    m = request.json['modifier']
    result = mash.mashup(original=o, modifier=m)
    return jsonify(result)