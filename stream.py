from config import *
import websocket, json 


#TODO I've implemented the methods to get the price for given stocks. now I need to do it for a collection of stocks.
#TODO And I also need to integrate this with DataPoints, so that I can get the advices!

socket = "wss://data.alpaca.markets/stream"

def on_open(ws):
    print("open")
    auth_data = {
        "action": "authenticate",
        "data": {"key_id": API_KEY, "secret_key": SECRET_KEY}
    }
    ws.send(json.dumps(auth_data))
    listen_message = {"action":"listen", "data": {"streams: [T.SPY]"}} #TAM for minute by minute.
    ws.send(json.dumps(listen_message))

def on_message(ws, message):
    print("reveived message")
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message)
   # ws.on_open = on_open
    ws.run_forever()
