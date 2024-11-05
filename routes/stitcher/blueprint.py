# Flask utils
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin

# Custom modules
from routes.stitcher import stitcher

stitcher_bp = Blueprint('stitcher', __name__, url_prefix = '/stitcher')



@stitcher_bp.route("/start/", methods = ["POST", "GET"])
@cross_origin()
def startVideo():
    data = request.get_json()
    try:
        stitcher.stitcherStart(data["command"])
        resp = jsonify(success= True)
        resp.status_code = 200
        return resp
    except:
        resp = jsonify(success= False)
        resp.status_code = 500
        return resp


@stitcher_bp.route("/stop/",  methods = ["POST"])
@cross_origin()
def stopVideo():
    try:
        stitcher.stitcherStop()
        resp = jsonify(success= True)
        resp.status_code = 200
        return resp
    except:
        resp = jsonify(success= False)
        resp.status_code = 500
        return resp