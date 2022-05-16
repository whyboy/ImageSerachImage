import imp
from flask import Flask, request, jsonify
from tinydb import TinyDB, Query
from flask_cors import CORS, cross_origin
from PIL import Image
from ImageSearch import searcher
import dbHelper

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

db = TinyDB('db.json')
query = Query()

samplePath="./Sample/image.PNG"
queryPath="./Pictures/"

obj = searcher("./Sample/image.PNG", "./Pictures/")
dbHelper.insertImageProperty()
# db.insert(
#     {
#     "id": 5809,
#     "BACKGROUND": "BLUE",
#     "CLOTHES": "N/A",
#     "EARRING": "GOLD HOOP",
#     "FUR": "SOLID GOLD",
#     "HAT": "N/A",
#     "MOUTH": "BORED"
# })

# db.insert(
#     {
#     "id": 5809,
#     "BACKGROUND": "BLUE",
#     "CLOTHES": "N/A",
#     "EARRING": "GOLD HOOP",
#     "FUR": "SOLID GOLD",
#     "HAT": "N/A",
#     "MOUTH": "BORED"
# })
@app.route('/')
def hello():
    return 'Hello, World!'

@app.route("/api/image", methods=["POST"])
@cross_origin()
def process_image():
    file = request.files['file']
    # Read the image via file.stream
    img = Image.open(file.stream)
    img.save('./Sample/image.PNG')
    comparisonImageList=obj.start()
    topMatchImageName=comparisonImageList[0][2]
    print(topMatchImageName.split('.')[0])
    print(db.search(query.id == topMatchImageName.split('.')[0]))
    bayc = db.search(query.id == topMatchImageName.split('.')[0])[0]

    result = {
        "ID": topMatchImageName.split('.')[0],
        "BACKGROUND": "N/A",
        "CLOTHES": "N/A",
        "EARRING": "N/A",
        "FUR": "N/A",
        "HAT": "N/A",
        "MOUTH": "N/A"
    }

    for key in bayc:
        result[key] = bayc[key]

    return jsonify(result)

    # return jsonify({'msg': 'success', 'size': [img.width, img.height]})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)