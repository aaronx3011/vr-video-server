# Flask utils
from flask import Blueprint, jsonify, request, render_template, current_app

# Custom modules
from routes.bucket import bucket


bucket_bp = Blueprint('bucket', __name__, url_prefix = '/bucket')

@bucket_bp.route("/clear/<string:folder>", methods = ["POST"])
def clearRecursive(folder):
    data = request.get_json()
    bucket.clearFilesByNameRecursive(folder, data["fileName"])
    resp = jsonify(success= True)
    resp.status_code = 200
    return resp

@bucket_bp.route("/sync/folder/", methods = ["GET"])
def syncFolderView():
    return render_template('syncFolderAWS.html', SERVER_IP = current_app.config['SERVER_IP'])

@bucket_bp.route("/sync/<string:folder>", methods = ["POST"]) 
def syncFolder(folder):
    bucket.syncFromAWSFolderToAWS(folder)
    resp = jsonify(success= True)
    resp.status_code = 200
    return resp