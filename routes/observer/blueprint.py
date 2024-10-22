# Flask utils
from flask import jsonify, Blueprint

# Custom modules
from routes.observer import observer

observer_bp = Blueprint('observer', __name__, url_prefix = '/observer')


@observer_bp.route("/start/")
def startObserver():
    try:
        observer.observerStart()
        resp = jsonify(success= True)
        resp.status_code = 200
        return resp
    except:
        resp = jsonify(success= False)
        resp.status_code = 500
        return resp

@observer_bp.route("/stop/")
def stopObserver():
    try:
        observer.observerStop()
        resp = jsonify(success = True)
        resp.status_code = 200
        return resp
    except:
        resp = jsonify(success= False)
        resp.status_code = 500
        return resp