# Network interactions
from logging import exception
import requests

# Flask util
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin

# Custom modules
from routes.stitcher import stitcher

stitcher_bp = Blueprint('stitcher', __name__, url_prefix = '/stitcher')


"""
TO DO:
    - DEBUG INFORMATION
    - ERROR HANDLING
    - RETURN GENERATED COMMAND TO THE CLIENT
"""

"""
{
    "streams": [

        {"streamConfiguration":
            {
                "needsStitch": false,
                "camera": {"cameraLink": "rtmp://192.168.88.60:1950/live/origin1", "codec": "264"},
                "streamName": "TESTING25MB15S265",
                "audioDevice": "0"
            }
        },
        {"streamConfiguration":
            {
                "needsStitch": false,
                "camera": {"cameraLink": "rtmp://192.168.88.60:1950/live/origin1", "codec": "264"},
                "streamName": "TESTING25MB15S265",
                "audioDevice": "0"
            }
        },
        {"streamConfiguration":
            {
                "needsStitch": false,
                "camera": {"cameraLink": "rtmp://192.168.88.60:1950/live/origin1", "codec": "264"},
                "streamName": "TESTING25MB15S265",
                "audioDevice": "0"
            }
        },




        {"streamConfiguration":
            {
                "needsStitch": true,
                "cameras": [
                    {"cameraLink": "rtmp://192.168.88.60:1950/live/origin1", "codec": "264"},
                    {"cameraLink": "rtmp://192.168.88.60:1950/live/origin1", "codec": "264"},
                    {"cameraLink": "rtmp://192.168.88.60:1950/live/origin1", "codec": "264"},
                    {"cameraLink": "rtmp://192.168.88.60:1950/live/origin1", "codec": "264"}],
                 "templateName": "LumixFullFrame.pts",
                 "streamName": "TESTING25MB15S265",
                 "audioDevice": "0"
            }
        }
    ]
}
"""




@stitcher_bp.route("/start/", methods = ["POST", "GET"])
@cross_origin()
def startVideo():
    data = request.get_json()
    try:
        print(data["streams"])
        stitcherCommand = stitcher.streamCommnadGenerator(data["streams"])
        print(stitcherCommand)
        stitcher.stitcherStart(stitcherCommand)
        resp = jsonify(success = True, generatedCommand = stitcherCommand)
        resp = jsonify(success = True, data=data)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
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







@stitcher_bp.route("/test/",  methods = ["GET"])
@cross_origin()
def test():
    try:



        resp = jsonify(success= True)
        resp.status_code = 200
        return resp
    except:
        resp = jsonify(success= False)
        resp.status_code = 500
        return resp
