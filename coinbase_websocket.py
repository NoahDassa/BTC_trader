import websocket
import json

def on_open(ws):
  
  #python dictionary

  subscribe_message =  {
    "type": "subscribe",
    "product_ids": [
        "BTC-USD"
    ],
    "channels": [
        "ticker"
    ]
  }

  #convert python dictionary to json data...

  ws.send(json.dumps(subscribe_message))

