import os

from flask_socketio import SocketIO

from shared.consts import INTERNAL_API_WEBSOCKETS_PORT
from shared.consts_secrets import miami_version_env_key


def handle_message(data):
    print('received message: ' + data)


def launch_socketio(flask_app):
    socketio_instance.on_event('ohlcv', handle_message)

    # realtime_prices_thread = Thread(name=f'realtime_prices', target=launch_realtime_prices_wrapper, args=(socketio,))
    # realtime_prices_thread.start()
