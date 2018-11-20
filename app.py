from flask import Flask, render_template, Response, jsonify

from camera_opencv import Camera

app = Flask(__name__)

control_json = [
    {
        "id": 1,
        "cmd": "run",
        "description": "control device run",
        "url_method":"post",
        "url_path":"xxxx//todo/api/v1/control/run",
        "url_param": "speed:,times",
        "url_param_type":"json",
        "url_param_demo":"{\"speed\":100,\"times\":5}"
    },
    {
        "id": 2,
        "cmd": "back",
        "description": "control device back",
        "url_method":"post",
        "url_path":"xxxx//todo/api/v1/control/back",
        "url_param": "speed:,times",
        "url_param_type":"json",
        "url_param_demo":"{\"speed\":100,\"times\":5}"
    },
    {
        "id": 3,
        "cmd": "stop",
        "description": "control device stop",
        "url_method":"post",
        "url_path":"xxxx//todo/api/v1/control/stop",
        "url_param": "None",
        "url_param_type":"json",
        "url_param_demo":""
    }
]


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


@app.route('/editor')
def editor():
    return render_template('editor.html')


@app.route('/todo/api/v1/control', methods=['POST'])
@app.route('/todo/api/v1/control/<string:control>', methods=['POST'])
def v1back(control=""):
    try:
        return "success"
    except Exception as e:
        return e


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=666, debug=True, threaded=True)
