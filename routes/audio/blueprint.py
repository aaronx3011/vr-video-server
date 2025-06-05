# Flask utils
from flask import Blueprint, jsonify 

# Custom modules
from routes.audio import audio

audio_bp = Blueprint('audio', __name__, url_prefix= '/audio')

@audio_bp.route("/record/devices/")
def recordDevices():
    print("=============== audio/record/devices/ ===============")
    resp = jsonify(audio.alsaRecordDevices())
    resp.status_code = 200
    return resp

