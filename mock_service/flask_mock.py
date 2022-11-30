import random
from flask import Flask, jsonify, request
import os

MOCK_HOST = os.getenv('MOCK_HOST')
MOCK_PORT = os.getenv('MOCK_PORT')

app = Flask(__name__)

VK_IDS_DATA = {}


@app.route('/vk_id/<username>', methods=['GET', 'POST'])
def vk_id(username):
    if request.method == 'GET':
        if username in VK_IDS_DATA:
            return jsonify(vk_id=VK_IDS_DATA.get(username)), 200
        else:
            return '', 404

    if request.method == 'POST':
        if username not in VK_IDS_DATA:
            id = random.randrange(1000000, 9999999)
            VK_IDS_DATA[username] = id
            return jsonify(status='success', vk_id=id), 201
        else:
            return jsonify(status='failed', error='already exists'), 304


if __name__ == '__main__':
    app.run(host=MOCK_HOST, port=MOCK_PORT)
