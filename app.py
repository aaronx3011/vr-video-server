#!/usr/bin/python3

# Enviroment interactions
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
    app.config['SERVER_IP'] = ''
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

    from routes.playfab import blueprint
    app.register_blueprint(blueprint.playfab_bp)

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

    from routes.audio import blueprint
    app.register_blueprint(blueprint.audio_bp)

    return app

app = createApp()
cors = CORS(app)
sio = SocketIO(app)


@app.route("/")
def videoStream():
    return render_template("index.html", SERVER_IP = app.config['SERVER_IP'])


if __name__ == '__main__':
    sio.run(app, host='0.0.0.0', debug = True, allow_unsafe_werkzeug=True)