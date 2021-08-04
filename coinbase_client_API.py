
from coinbase.wallet.client import Client


client = Client('C7dmST675aKMOMSz','OOxYtAUYlJOnyCY4eaxe4Egg6GkZIzM9',api_version='2018-03-22')
payment_method = client.get_payment_methods()[0]
account = client.get_primary_account()
buy_price = float(client.get_buy_price(currency = 'USD').amount)
sell_price = float(client.get_sell_price(currency = 'USD').amount)
