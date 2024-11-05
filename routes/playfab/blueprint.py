# Flask utils
from flask import Blueprint, jsonify, request, render_template
from werkzeug.utils import secure_filename

# Own modules
from routes.playfab import playfabConnector


playfab_bp = Blueprint('playfab', __name__, url_prefix = '/playfab')

@playfab_bp.route("/stream/<string:tag>/off/")
def turnOffStreams(tag):
    try:
        playfabConnector.turnOffItems(tag)
        resp = jsonify(success= True)
        resp.status_code = 200
        return resp
    except:
        resp = jsonify(success= False)
        resp.status_code = 500
        return resp


@playfab_bp.route("/stream/get/names")
def get_names():
    return playfabConnector.GetItems()


@playfab_bp.route("/stream/<string:tag>/on/")
def turnOnStreams(tag):
    try:
        playfabConnector.turnOnItems(tag)
        resp = jsonify(success= True)
        resp.status_code = 200
        return resp
    except:
        resp = jsonify(success= False)
        resp.status_code = 500
        return resp
    