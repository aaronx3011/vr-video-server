# Flask utils
from flask import Blueprint, jsonify 
from flask_cors import cross_origin

# Custom modules
from routes.resources import resources as rs
from routes.observer import observer
from routes.stitcher import stitcher
from routes.bucket import bucket

resources_bp = Blueprint('resources', __name__, url_prefix= '/resources')

@resources_bp.route("/usage/")
def resources():
        resp = jsonify(rs.utilization())
        resp.status_code = 200
        return resp

@resources_bp.route("/process/status/")
@cross_origin()
def statusVideo():
    resp = jsonify(active = stitcher.VIDEO["active"], text = stitcher.VIDEO["output"], observerText = observer.OBSERVER['output'])
    resp.status_code = 200
    return resp 


@resources_bp.route("/process/aws/status/")
@cross_origin()
def statusAWS():
    resp = jsonify(active = bucket.AWS["active"], text = bucket.AWS["output"])
    resp.status_code = 200
    return resp 