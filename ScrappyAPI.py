from Scrappy import scrap
from flask import Flask, jsonify, request
import json

app = Flask(__name__)


@app.route('/scrappy', methods=['POST', 'GET'])
def scrap_post():
    return jsonify(scrap(json.loads(request.data)))

if __name__ == '__main__':
    app.run(debug=False)
