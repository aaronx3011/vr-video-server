# Flask utils
from flask import Blueprint, jsonify, request, render_template, current_app
from flask_cors import cross_origin


from routes.calibration import calibration


# Constants
calibration_bp = Blueprint('calibration', __name__, url_prefix='/calibration')


@calibration_bp.route("/", methods = ['POST','GET'])
@cross_origin()
def Calibration():
    if request.method == "GET":
        return render_template("calibration.html", SERVER_IP = current_app.config["SERVER_IP"], SERVER_PORT = current_app.config['SERVER_PORT'])

    if request.method == "POST":
        data = request.get_json()
        print(data["cameras"])
        filesSuffix = calibration.takeSnapshotStartCommand(data["cameras"])
        resp = jsonify(success = True, imagesNames = filesSuffix)
        resp.status_code = 200
        return resp
