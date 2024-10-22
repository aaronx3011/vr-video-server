# Flask utils
from flask import jsonify, Blueprint

# Custom modules
from routes.audio import audio

audio_bp = Blueprint('audio', __name__, url_prefix = '/audio')

@audio_bp.route("/status/")
def statusLoopback():
    try:
        resp = jsonify(IsActive = audio.loopbackIsActive())
        resp.status_code = 200
        return resp
    except:
        resp = jsonify(success = False)
        resp.status_code = 500
        return resp

@audio_bp.route("/activate/")
def activateLoopback():
    try:
        if not audio.loopbackIsActive():
            audio.loopbackStart()
        resp = jsonify(success= True)
        resp.status_code = 200
        return resp
    except:
        resp = jsonify(success = False)
        resp.status_code = 500
        return resp

@audio_bp.route("/deactivate/")
def deactivateLoopback():
    try:
        audio.loopbackEnd()
        resp = jsonify(success= True)
        resp.status_code = 200
        return resp
    except:
        resp = jsonify(success = False)
        resp.status_code = 500
        return resp