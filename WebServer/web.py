from bson import json_util
import json
import datetime
import sys
from flask import request
from flask import Flask,render_template
from flask_pymongo import PyMongo
from flask import jsonify

def default(o):
  if type(o) is datetime.date or type(o) is datetime.datetime:
    return o.isoformat()

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/temple"
mongo = PyMongo(app)

@app.route('/<string:page_name>/')
def render_static(page_name):
    return render_template('%s.html' % page_name)

@app.route('/blogs', methods=['POST'])
def post_blogs():
  title = request.form.get('title')
  author = request.form.get('author')
  description = request.form.get('description')
  doc = mongo.db.blogs.insert({'title':title,'author':author,'description':description,"published_on": datetime.now()})
  return "Inserted"

@app.route('/blogs', methods=['GET'])
def get_blogs():
 api_response = {}
 api_response["status_code"] = "success"
 api_response["message"]="success"
 #api_response["posts"] ={}
 #api_response["posts"]["status_code"] = "success"
 #api_response["posts"]["message"]="success"
 #api_response["posts"]["data"] = db_response
 db_response = list(mongo.db.blogs.find({}))
 api_response["data"] = []
 for response in db_response:
    print "response",response.keys()
    formatted_response = {}
    formatted_response["id"] = str(response["_id"])
    formatted_response["title"] = response["title"]
    formatted_response["author"] = response["author"]
    formatted_response["description"] = response["description"]
    formatted_response["published_at"] = response["published_on"]
    formatted_response["img_url"] = "http://www.google.com"
    formatted_response["blog_url"] = "http://www.google.com"
    api_response["data"].append(formatted_response)
 #api_response["posts"]["data"] = db_response
 #api_response = jsonify(api_response)
 #api_response =  json.dumps(api_response,sort_keys=True,
  #indent=1,default=default)
 return jsonify(api_response)

if __name__ == '__main__':
   app.run('0.0.0.0',debug=True , port=int(sys.argv[1]))
