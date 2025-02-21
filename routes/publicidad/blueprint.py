# Flask utils
from flask import Blueprint, jsonify, request, render_template, current_app
from werkzeug.utils import secure_filename

# Shell commands
import subprocess
import shlex

# PC interactions
import os
from dotenv import load_dotenv

load_dotenv(".env")

# Constants
DEFAULT_BUCKET_LINK = os.getenv("DEFAULT_BUCKET_LINK") 
PUBLICIDAD = {'active': False, 'output': ''}
UPLOAD_ADD_FOLDER = './publicidad'

publicidad_bp = Blueprint('publicidad', __name__, url_prefix='/publicidad')

def publicidadStart(command) -> bool:
    if PUBLICIDAD['active'] == False:
        try:
            process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
            PUBLICIDAD["active"] = True
            for line in process.stdout:
                PUBLICIDAD["output"] = line[:-1]
                
            process = subprocess.Popen(['aws', 's3', 'sync', f'./{UPLOAD_ADD_FOLDER}', f'{DEFAULT_BUCKET_LINK}publicidad/low/'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
            for line in process.stdout:
                PUBLICIDAD["output"] = line[:-1]

            PUBLICIDAD["active"] = False
            PUBLICIDAD["output"] = ''
        except subprocess.CalledProcessError as e:
            return False
    return True





@publicidad_bp.route("/")
def publicidad():
    return render_template("cargarPublicidad.html", SERVER_IP = current_app.config["SERVER_IP"], SERVER_PORT = current_app.config['SERVER_PORT'])


@publicidad_bp.route('/upload/', methods=['POST'])
def uploadAdd():
    try:
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_ADD_FOLDER, filename))
        resp = jsonify(success= True)
        resp.status_code = 200
        return resp
    except:
        resp = jsonify(success= False)
        resp.status_code = 500
        return resp
    

@publicidad_bp.route("/start/", methods = ["POST"])
def startPublicidad():
    data = request.get_json()
    if publicidadStart(data["command"]):
        resp = jsonify(success= True)
        resp.status_code = 200
        return resp
    else:
        resp = jsonify(success= False)
        resp.status_code = 500
        return resp


@publicidad_bp.route("/status/")
def statusPublicidad():
    resp = jsonify(active = PUBLICIDAD['active'], text = PUBLICIDAD['output'])
    resp.status_code = 200
    return resp