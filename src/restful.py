#!flask/bin/python
from flask import Flask, jsonify
from flask import make_response
from flask import request
from werkzeug.contrib.cache import MemcachedCache

app = Flask(__name__)

cache = MemcachedCache("http://facial-recognition-hack.herokuapp.com")

faces = [
    {
        'name': "Bob",
        'time': "123"
    }
]
@app.route('/facial/api/v1.0/faces/get', methods=['GET'])
def get_faces():
    faces = cache.get('faces')
    return jsonify({'faces': faces})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/facial/api/v1.0/faces/post', methods=['POST'])
def create_face():
    # if not request.json or not 'faces' in request.json:
    #     quit(400)
    face = {
        'name': request.json['name'],
        'time': request.json['time']
    }

    cache.set('faces', face, timeout=5 * 60)
    faces.append(face)
    # return jsonify({'face': face}), 201
    return ''

if __name__ == '__main__':
    app.run(debug=True)