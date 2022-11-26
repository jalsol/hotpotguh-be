from flask import Flask, app, request, jsonify

app = Flask(__name__)


# @app.route('/predict/', methods=['POST'])
# def send_image():


@app.route('/test/', methods=['GET'])
def test():
    payload = {
        'Status': 'Success',
        'Message': 'haha brrrr'
    }

    return jsonify(payload)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=False)
