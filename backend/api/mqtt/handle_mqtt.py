import json

from flask_socketio import SocketIO, join_room, leave_room

from api.last_ohlcv_database import last_ohlcv_database
from shared.consts import OHLCV_SOCKETIO_EVENT_NAME


def room_name_generator(exchange: str, timeframe: str, symbol: str):
    return f'{exchange}:{symbol}:{timeframe}'


def handle_ohlcv_realtime_candles(socket: SocketIO, mqtt):
    mqtt.subscribe('ohlcv')

    @socket.on('join')
    def on_join(data):
        join_room(data)

    @socket.on('leave')
    def on_leave(data):
        leave_room(data)

    @mqtt.on_message()
    def handle_mqtt_message(client, userdata, message):
        if message.topic == OHLCV_SOCKETIO_EVENT_NAME:
            exchange = json.loads(message.payload.decode())['exchange']
            symbol = json.loads(message.payload.decode())['symbol']
            timeframe = json.loads(message.payload.decode())['timeframe']

            room = room_name_generator(exchange, timeframe, symbol)
            data = {'exchange': exchange,
                    'timeframe': timeframe,
                    'symbol': symbol,
                    'ohlcv': [json.loads(message.payload.decode())['timestamp'],
                              json.loads(message.payload.decode())['open'],
                              json.loads(message.payload.decode())['high'],
                              json.loads(message.payload.decode())['low'],
                              json.loads(message.payload.decode())['close'],
                              json.loads(message.payload.decode())['volume']]}
            last_ohlcv_database[room] = data
            socket.emit(OHLCV_SOCKETIO_EVENT_NAME, data, to=room)
