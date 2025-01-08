from pymongo import MongoClient
import redis
from flask import Flask, request, jsonify
from bson import ObjectId


mongo_client = MongoClient('mongodb://localhost:27017/')
db = mongo_client['test_db']
col = db["entities"]

app = Flask(__name__)

redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

@app.route("/getall", methods=["GET"])
def get_all():
    cache_key = "all_entities"
    cached_data = redis_client.get(cache_key)
    if cached_data:
        print("Getting data from cache...")
        return jsonify(eval(cached_data)), 200
    
    print("Getting data from database...")
    entities = list(col.find())
    for entity in entities:
        entity["_id"] = str(entity["_id"])

    redis_client.setex(cache_key, 120, str(entities))
    print("Cache updated")

    return jsonify(entities), 200

@app.route("/getbyid", methods=["GET"])
def get_by_id():
    id = request.args.get('_id')
    cache_key = f"entity_{id}"
    cached_data = redis_client.get(cache_key)
    if cached_data:
        print("Getting data from cache...")
        return jsonify(eval(cached_data)), 200

    print("Getting data from database...")
    result = col.find_one({"_id":ObjectId(id)})
    result["_id"] = str(result["_id"])
    redis_client.setex(cache_key, 120, str(result))
    print("Cache updated")

    return jsonify(result), 200

@app.route("/insert", methods=["POST"])
def insert():
    content = request.get_json()
    result = col.insert_one(content)
    print("Inserting to database...")
    redis_client.delete("all_entities")
    print("Deleting entities from cache...")
    return jsonify({"message": "Inserted successfully"}), 201

@app.route("/delete", methods=["DELETE"])
def delete():
    content = request.get_json()
    result = col.delete_one({"_id":ObjectId(content["_id"])})
    print("Deleting from database...")
    if result.deleted_count > 0:
        redis_client.delete("all_entities")
        redis_client.delete(f"entity_{content['_id']}")
        print("Deleting entity from cache...")
        return jsonify({"message": "Deleted successfully"}), 200
    else:
        return jsonify({"error": "Not found"}), 404

@app.route("/update", methods=["PUT"])
def update():
    id = request.args.get('_id')
    content = request.get_json()
    value = {"$set":{"name":content["name"]}}
    result = col.update_one({"_id":ObjectId(id)}, value)
    print("Updating in database...")
    if result.matched_count > 0:
        redis_client.delete("all_entities")
        redis_client.delete(f"entity_{id}")
        print("Deleting entity from cache...")
        return jsonify({"message": "Updated successfully"}), 200
    else:
        return jsonify({"error": "Not found"}), 404

if __name__ == '__main__':
    app.run()