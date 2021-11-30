# mongo.py

from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'Maindb'
app.config['MONGO_URI'] = \
  'mongodb+srv://admin:cAUm4f8cffJuucQ@ecocluster.3lana.mongodb.net/maindb?retryWrites=true&w=majority'
mongo = PyMongo(app)
permitted = ["type", "name", "district", "description", "latitude", "longitude", "phone", "site", "image"]


@app.route('/getall', methods=['GET'])
def get_all_items():
  agro = mongo.db.AgroUsad
  output = []
  for s in agro.find():
    out = {}
    out.update((key, val) for (key, val) in s.items() if key in permitted)
    output.append(out)
  return jsonify({'result': output})


@app.route("/")
def home_view():
  return "<h1>Welcome to Eco Backend</h1>"


@app.route('/getbyname/', methods=['POST'])
def get_one_by_name():
  agro = mongo.db.AgroUsad
  s = agro.find_one({'name': request.json['name']})
  if s:
    out = {}
    out.update((key, val) for (key, val) in s.items() if key in permitted)
    return jsonify({'result': out})
  else:
    output = "No such name"
  return jsonify({'result': output})


@app.route('/getbytype/', methods=['POST'])
def get_one_by_type():
  agro = mongo.db.AgroUsad
  s = agro.find_one({'type': request.json['type']})
  if s:
    out = {}
    out.update((key, val) for (key, val) in s.items() if key in permitted)
    return jsonify({'result': out})
  else:
    output = "No such name"
  return jsonify({'result': output})


@app.route('/addnew', methods=['POST'])
def add_new():
  agro = mongo.db.AgroUsad
  print(request.get_json())
  agro_id = agro.insert(request.get_json())
  new_agro = agro.find_one({'_id': agro_id})
  return jsonify({'result': "success"})


# delete
@app.route('/deletebyname', methods=['POST'])
def delete_one():
  agro = mongo.db.AgroUsad
  s = agro.find_one({'name': request.json['name']})
  if s:
    agro.delete_one(s)
    return jsonify({'result': "success"})
  else:
    output = "No such name"
  return jsonify({'result': output})


# edit
@app.route('/update/', methods=['PUT'])
def update_one(name):
  agro = mongo.db.AgroUsad
  s = agro.find_one({"name": name})
  if s:
    # Values to be updated.
    new_values = {"$set": request.get_json()}
    agro.updateOne({s}, new_values)
    return jsonify({'result': "success"})
  else:
    output = "No such name"
  return jsonify({'result': output})
