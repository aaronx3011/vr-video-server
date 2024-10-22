# Flask utils
from flask import (
    Blueprint, jsonify,
    request, send_from_directory,
    render_template, current_app
)
from flask_cors import cross_origin
from werkzeug.utils import secure_filename

# PC interactions
import os
import sys

# Custom modules
from routes.file import createMaster
from routes.file import clearLocalFolder

# Constants

file_bp = Blueprint('file', __name__, url_prefix='/file')

UPLOAD_TEMPLATE_FOLDER = './stitch-templates'
BANNERS_UPLOAD_FOLDER = './banners'

@file_bp.route("/<string:filename>")
def get_image(filename):
    return send_from_directory(os.getcwd() + "/", path=filename, as_attachment=False)



@file_bp.route("/preview/<string:filename>")
@cross_origin()
def get_preview(filename):
    return send_from_directory(os.getcwd() + "/preview/", path=filename, as_attachment=False)


@file_bp.route("/videos/low/<string:filename>")
@cross_origin()
def get_video(filename):
    return send_from_directory(os.getcwd() + "/videos/low/", path=filename, as_attachment=False)


@file_bp.route("/create/master", methods=['POST'])
@cross_origin()
def createMast():
    data = request.get_json()

    if createMaster.writeFile(createMaster.createFile(data["fileName"]),data["streams"]):
        resp = jsonify(success= True)
        resp.status_code = 200
        return resp

    else:
        resp = jsonify(success= False)
        resp.status_code = 500
        return resp


@file_bp.route("/clear/videos")
def clear():
    try:
        clearLocalFolder.clearLocal()
        resp = jsonify(success= True)
        resp.status_code = 200
        return resp

    except:
        resp = jsonify(success= False)
        resp.status_code = 500
        return resp


@file_bp.route('/template/upload/', methods=['POST'])
def uploadTemplate():
    try:
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_TEMPLATE_FOLDER, filename))
        resp = jsonify(success= True)
        resp.status_code = 200
        return resp
    except:
        resp = jsonify(success= False)
        resp.status_code = 500
        return resp


@file_bp.route('/upload/', methods = ['GET', 'POST'])
def uploadFiles():
    if request.method == 'POST':
        files = request.files.getlist("file")
        for file in files:
            newFileName = secure_filename(file.filename)
            file.save(os.path.join(BANNERS_UPLOAD_FOLDER, newFileName))

        resp = jsonify(success= True)
        resp.status_code = 200
        return resp

    if request.method == 'GET':
        return render_template("uploadFile.html", SERVER_IP = current_app.config["SERVER_IP"])