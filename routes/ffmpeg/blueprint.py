# Flask utils
from flask import jsonify, Blueprint

# Custom modules
from routes.ffmpeg import ffmpeg

ffmpeg_bp = Blueprint('ffmpeg', __name__, url_prefix = '/ffmpeg')

@ffmpeg_bp.route("/installed/")
def installed():
    if ffmpeg.ffmpegInstalled():
        resp = jsonify(success= True)
        resp.status_code = 200
        return resp
    else:
        resp = jsonify(success= False)
        resp.status_code = 500
        return resp

@ffmpeg_bp.route("/version/")
def version():
    try:
        resp = jsonify(ffmpeg.ffmpegVersion())
        resp.status_code = 200
        return resp
    except:
        resp = jsonify(success = False)
        resp.status_code = 500
        return resp