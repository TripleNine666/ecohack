# mongo.py

from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'Maindb'
app.config['MONGO_URI'] = \
  'mongodb+srv://TripleNine:oBuQDEujor84HtKW@cluster0.trbei.mongodb.net/Maindb?retryWrites=true&w=majority'
mongo = PyMongo(app)


@app.route('/agro', methods=['GET'])
def get_all_stars():
  agro = mongo.db.AgroUsad
  output = []
  for s in agro.find():
    output.append({
      'name': s['name'],
      'district': s['district'],
      'address': s['address']
    })
  return jsonify({'result': output})


@app.route('/agro/', methods=['GET'])
def get_one_star(name):
  agro = mongo.db.AgroUsad
  s = agro.find_one({'name': name})
  if s:
    output = {
      'name': s['name'],
      'district': s['district'],
      'address': s['address']
    }
  else:
    output = "No such name"
  return jsonify({'result': output})


@app.route('/agro', methods=['POST'])
def add_star():
  agro = mongo.db.AgroUsad
  name = request.json['name']
  district = request.json['district']
  agro_id = agro.insert({'name': name, 'district': district})
  new_agro = agro.find_one({'_id': agro_id})
  output = {'name': new_agro['name'], 'district': new_agro['district']}
  return jsonify({'result': output})


if __name__ == '__main__':
    app.run(debug=True)
