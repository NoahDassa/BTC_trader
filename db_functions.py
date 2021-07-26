from db_connection import *
from coinbase_websocket import *



def start_ledger(strategy_id,current_price,amount,BTC,time):

  db.strategies.update_one({'_id':strategy_id},{'$push':
   {'order':
   {'count':1,
     'buy_sell':'buy', 
     'price': current_price,
     'amount':amount,
     'BTC':BTC,
     
     'profit': 0,
     
     'increase': 0,
     'decrease' : 0,
     'time' : time
    }
    }},upsert=True)        

def buy_ledger(strategy_id,count,current_price,amount,BTC,increase,decrease,time):

   db.strategies.update_one({'_id':strategy_id},{'$push':
   {'order':
   {'count':count,
     'buy_sell':'buy', 
     'price': current_price,
     'amount':amount,
     'BTC':BTC,
     
     'profit': "no change",
     
     'increase': increase,
     'decrease' : decrease,
     'time' : time 
    }
    }},upsert=True)

def sell_ledger(strategy_id,count,current_price,amount,BTC,profit,increase,decrease,time):
  
   db.strategies.update_one({'_id':strategy_id},{'$push':
   {'order':
   {'count':count,
     'buy_sell':'sell', 
     'price': current_price,
     'amount': amount,
     'BTC': BTC,

     'profit':profit,
     
     'increase': increase,
     'decrease' : decrease,
     'time' : time
    }
    }},upsert=True)