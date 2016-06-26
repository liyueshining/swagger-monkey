from flask import Flask, jsonify
from flask import request
from entity.UrlInfo import UrlInfo

app = Flask(__name__)

@app.route('/urls', methods=['GET', 'POST', 'DELETE'])
def urls_service(infos=None):
    if request.method == 'GET':
        info = UrlInfo()
        return jsonify(info)
