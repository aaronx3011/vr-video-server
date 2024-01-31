import subprocess
# import tempfile
from flask import Flask, render_template, jsonify, request, url_for, redirect
import psutil
import shlex
# import nvsmi
# import nvidia_smi

from flask_cors import CORS, cross_origin



VIDEO = {'active': False, 'output': ''}
OBSERVER = {'active': False, 'output': ''}


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


def ffmpegInstalled() -> bool:
    try:
        subprocess.check_call(['ffmpeg', '-version'], stdout= subprocess.PIPE)
        return True
    except subprocess.CalledProcessError as e:
        return False
    

def ffmpegVersion() -> jsonify:
    try:
        proc = subprocess.Popen(['ffmpeg', '-version'], stdout=subprocess.PIPE).communicate()[0]
        resp = jsonify(proc.decode("utf-8")[:-1].split("\n"))
        resp.status_code = 200
        return resp

    except subprocess.CalledProcessError as e:
        resp = jsonify(success= False)
        resp.status_code = 500
        return resp


def ffmpegStart(ffmpegCommand) -> bool:
    if VIDEO['active'] == False:
        try:
            process = subprocess.Popen(shlex.split(ffmpegCommand), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
            print(ffmpegCommand)
            VIDEO["active"] = True
            for line in process.stdout:
                VIDEO["output"] = line[:-1]
            VIDEO["active"] = False
            VIDEO["output"] = ''
        except subprocess.CalledProcessError as e:
            return False
    return True


def observerStart() -> bool:
    if OBSERVER['active'] == False:
        try:
            process = subprocess.Popen(['./observer.sh'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
            OBSERVER["active"] = True
            for line in process.stdout:
                OBSERVER["output"] = line[:-1]
            OBSERVER["active"] = False
            OBSERVER["output"] = ''
        except subprocess.CalledProcessError as e:
            return False
    return True



def ffmpegStop() -> bool:
    try:
        subprocess.check_call(['pkill', 'ffmpeg'], stdout= subprocess.PIPE)
        VIDEO['active'] = False
        VIDEO['output'] = ''
        return True
    except subprocess.CalledProcessError as e:
        return False




def observerStop() -> bool:
    try:
        subprocess.check_call(['pkill', 'inotify'], stdout= subprocess.PIPE)
        return True
    except subprocess.CalledProcessError as e:
        return False


def awsStop() -> bool:
    try:
        subprocess.check_call(['pkill', 'aws'], stdout= subprocess.PIPE)
        return True
    except subprocess.CalledProcessError as e:
        return False


def utilization() -> jsonify:
    try:
        proc = subprocess.Popen(
            [
                'nvidia-smi',
                '--query-gpu=utilization.gpu,utilization.memory,utilization.decoder,utilization.encoder',
                '--format=csv'

            ],
            stdout=subprocess.PIPE
        ).communicate()[0]
        keys = proc.decode("utf-8")[:-1].split("\n")[0].split(", ")
        values = proc.decode("utf-8")[:-1].split("\n")[1].split(", ")
        res = {
            "utilization.cpu [%]" : psutil.cpu_percent(),
            "utilization.ram [%]" : psutil.virtual_memory().percent
            }
        i= 0
        for key in keys:
            res[key] = float(values[i][:-2])
            i += 1
        
        resp = jsonify(res)
        resp.status_code = 200
        # resp.headers.add('Access-Control-Allow-Origin', '*')
        return resp

    except subprocess.CalledProcessError as e:
        resp = jsonify(success= False)
        resp.status_code = 500
        return resp





@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ffmpeg/installed/")

def installed():

    if ffmpegInstalled():
        resp = jsonify(success= True)
        resp.status_code = 200
        return resp
    else:
        resp = jsonify(success= False)
        resp.status_code = 500
        return resp

@app.route("/ffmpeg/version/")
def version():
    return ffmpegVersion()


@app.route("/ffmpeg/status/")
def statusVideo():
    
    resp = jsonify(active = VIDEO['active'], text = VIDEO['output'], observerText = OBSERVER['output'])
    resp.status_code = 200
    # resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp


@app.route("/ffmpeg/start/", methods = ["POST", "GET"])
def startVideo():
    resp = jsonify(success= True)
    # resp.headers.add('Access-Control-Allow-Origin', '*')
    resp.status_code = 200
    data = request.get_json()
    if ffmpegStart(data["command"]):
        print ("estamos aqui")
        resp = jsonify(success= True)
        # resp.headers.add('Access-Control-Allow-Origin', '*')
        resp.status_code = 200
        return resp
    else:
        resp = jsonify(success= False)
        resp.status_code = 500
        # resp.headers.add('Access-Control-Allow-Origin', '*')
        return resp


@app.route("/observer/start/")
def startObserver():
    if observerStart():
        resp = jsonify(success= True)
        # resp.headers.add('Access-Control-Allow-Origin', '*')
        resp.status_code = 200
        return resp
    else:
        resp = jsonify(success= False)
        # resp.headers.add('Access-Control-Allow-Origin', '*')
        resp.status_code = 500
        return resp



@app.route("/ffmpeg/stop/")
def stopVideo():
    if ffmpegStop():
        resp = jsonify(success= True)
        resp.status_code = 200
        # resp.headers.add('Access-Control-Allow-Origin', '*')

        return resp
    else:
        resp = jsonify(success= False)
        resp.status_code = 500
        # resp.headers.add('Access-Control-Allow-Origin', '*')

        return resp



@app.route("/observer/stop/")
def stopObserver():
    # resp.headers.add('Access-Control-Allow-Origin', '*')
    if observerStop():
        resp = jsonify(success= True)
        resp.status_code = 200
        return resp
    else:
        resp = jsonify(success= False)
        resp.status_code = 500
        return resp
    

@app.route("/aws/stop/")
def stopBucket():
    if awsStop():
        resp = jsonify(success= True)
        resp.status_code = 200
        # resp.headers.add('Access-Control-Allow-Origin', '*')
        return resp
    else:
        resp = jsonify(success= False)
        # resp.headers.add('Access-Control-Allow-Origin', '*')
        resp.status_code = 500
        return resp

@app.route("/resources/")
def resources():
    return utilization()

@app.route("/chart/")
def chart():
    return render_template("chart.html")

