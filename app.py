#!/usr/bin/python3

# Enviroment interactions
import os
from dotenv import load_dotenv

# Flask utils
from flask import Flask, render_template
from flask_cors import CORS
from flask_socketio import SocketIO

# Custom modules
from customUtils import net

# Constants
load_dotenv('.env')

# App
def createApp():
    app = Flask(__name__)
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['SERVER_PORT'] = os.getenv("SERVER_PORT")
    app.config['SERVER_IP'] = ''
    app.config['DEBUG'] = os.getenv("DEBUG")

    if app.config['DEBUG'] == True:
        app.config['SERVER_IP'] = os.getenv("SERVER_IP")
    else:
        while True:
            try:
                app.config['SERVER_IP'] = net.getLocalIPv4()
            except:
                pass
            finally:
                if app.config['SERVER_IP'] !='':
                    break


    from routes.publicidad import blueprint
    app.register_blueprint(blueprint.publicidad_bp)

    from routes.vrseat import blueprint
    app.register_blueprint(blueprint.vrseat_bp)

    from routes.file import blueprint
    app.register_blueprint(blueprint.file_bp)

    from routes.ffmpeg import blueprint
    app.register_blueprint(blueprint.ffmpeg_bp)

    from routes.resources import blueprint
    app.register_blueprint(blueprint.resources_bp)

    from routes.bucket import blueprint
    app.register_blueprint(blueprint.bucket_bp)

    from routes.observer import blueprint
    app.register_blueprint(blueprint.observer_bp)

    from routes.stitcher import blueprint
    app.register_blueprint(blueprint.stitcher_bp)

    from routes.calibration import blueprint
    app.register_blueprint(blueprint.calibration_bp)

    from routes.audio import blueprint
    app.register_blueprint(blueprint.audio_bp)

    return app

app = createApp()
cors = CORS(app)
sio = SocketIO(app)


@app.route("/")
def videoStream():
    return render_template("index.html", SERVER_PORT=app.config['SERVER_PORT'], SERVER_IP = app.config['SERVER_IP'] )


if __name__ == '__main__':
    sio.run(app, host='0.0.0.0', port= app.config['SERVER_PORT'], debug = True, allow_unsafe_werkzeug=True)
