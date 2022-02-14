import requests
import websocket

token = "c8028daad3i8n3bh94dg"

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    ws.send('{"type":"subscribe","symbol":"AAPL"}')
    ws.send('{"type":"subscribe","symbol":"AMZN"}')
    ws.send('{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}')
    ws.send('{"type":"subscribe","symbol":"IC MARKETS:1"}')

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://ws.finnhub.io?token="+token,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()

# token = "c8028daad3i8n3bh94dg"
# # Register new webhook for earnings
# r = requests.post('https://finnhub.io/api/v1/webhook/add?token='+token, json={'event': 'earnings', 'symbol': 'AAPL'})
# res = r.json()
# print(res)

# webhook_id = res['id']
# # List webhook
# r = requests.get('https://finnhub.io/api/v1/webhook/list?token='+token)
# res = r.json()
# print(res)

# #Delete webhook
# r = requests.post('https://finnhub.io/api/v1/webhook/delete?token='+token, json={'id': webhook_id})
# res = r.json()
# print(res)