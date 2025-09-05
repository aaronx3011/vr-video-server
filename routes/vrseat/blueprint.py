# Flask utils
from flask import Blueprint, jsonify

# Own modules
from routes.vrseat import vrseat


vrseat_bp = Blueprint('vrseat', __name__, url_prefix = '/vrseat')



@vrseat_bp.route("/streams/")
def get_names():
    print("+++++++++++++++++++++++++++++ VRSEAT/STREAM/NAMES +++++++++++++++++++++++++++++")
    try:
        resp = jsonify(vrseat.getInventory())
        resp.status_code = 200
        return resp
    except:
        print("FAILED")
        resp = jsonify(success= False)
        resp.status_code = 500
        return resp


@vrseat_bp.route("/stream/<string:itemId>/off/")
def turnOffStreams(itemId):
    try:
        vrseat.turnOffItems(itemId)
        resp = jsonify(success= True)
        resp.status_code = 200
        return resp
    except:
        resp = jsonify(success= False)
        resp.status_code = 500
        return resp



@vrseat_bp.route("/stream/<string:itemId>/on/")
def turnOnStreams(itemId):
    try:
        vrseat.turnOnItems(itemId)
        resp = jsonify(success= True)
        resp.status_code = 200
        return resp
    except:
        resp = jsonify(success= False)
        resp.status_code = 500
        return resp
