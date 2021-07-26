
from db_connection import *
from db_functions import *
from coinbase_websocket import *



def on_message(ws, message):
  
  info =json.loads(message)


  for A in range(1,10):
    for a in range(3,5):
      for e in range(1,10):

        strategy_id = 'initial_investment_'+str(100*A)+'_exponent_base_'+str(a)+'_brick_gap'+str(e)
        time = info['time']
        print(strategy_id)
        
        if db.strategies.count_documents({'_id' : strategy_id}) == 0:
          
          print('no document exists yet for this strategy')
          
          current_price= float(info['price'])
          amount = float(100*A)
          BTC = (amount/current_price)*.99925
          print(BTC,' bitcoin purchased @ ',current_price,' for ',amount,' USD')
          
          start_ledger(strategy_id,current_price,amount,BTC,time)
          print('----ledger started for this strategy----')
        
        else:
          
          print('document exists')

          count = len(db.strategies.find_one({'_id':strategy_id})['order'])
          print('the count is ',count)
          
          current_price = float(info['price'])
          brick_price = float(db.strategies.find_one({'_id':strategy_id})['order'][count-1]['price'])
          print('current price is ==',current_price,'== brick price is ==',brick_price,'==')

          increase   = float(db.strategies.find_one({'_id':strategy_id})['order'][count-1]['increase'])
          decrease   = float(db.strategies.find_one({'_id':strategy_id})['order'][count-1]['decrease'])
          print('the increase is ',increase,' and the decrease is ',decrease)





          if current_price < brick_price * (1-(float(e)*3/1000)):
            print('brick price decreasing by 3/10 of a percent of e. e is ', e)
            
            increase = 0
            decrease += 1
            count += 1

           
            BTC = db.strategies.find_one({'_id':strategy_id})['order'][count-2]['BTC']
      
            amount = BTC * current_price*.99925
            if count <= 2:
              profit = amount - db.strategies.find_one({'_id':strategy_id})['order'][count-2]['amount']
            else:
              previous_profit =  float(db.strategies.find_one({'_id':strategy_id})['order'][count-3]['profit']) 
              profit = previous_profit + amount - db.strategies.find_one({'_id':strategy_id})['order'][count-2]['amount']
            
            print('profit of ',profit,'from ',BTC,' bitcoin @',current_price,' for ', amount)

            sell_ledger(strategy_id,count,current_price,amount,BTC,profit,increase,decrease,time)
            print('--sell ledger made--')
            
            count += 1
            amount = float(100 * A * pow(a,decrease))
            BTC = amount/current_price
            
            buy_ledger(strategy_id,count,current_price,amount,BTC,increase,decrease,time)
            print('--buy ledger made--')






          if current_price > brick_price * (1+(float(e)*3/1000)):
            print('brick price increasing by 1/5 of a percent of e. e is ', e)
            
            increase += 1
            decrease = 0
            count += 1


            BTC = db.strategies.find_one({'_id':strategy_id})['order'][count-2]['BTC']

            amount = BTC * current_price *.99925
            if count <= 2:
              profit = amount - db.strategies.find_one({'_id':strategy_id})['order'][count-2]['amount']
            else:
              previous_profit =  float(db.strategies.find_one({'_id':strategy_id})['order'][count-3]['profit'])
              profit = previous_profit + amount  - db.strategies.find_one({'_id':strategy_id})['order'][count-2]['amount']
            
            print('profit of ',profit,'from ',BTC,' bitcoin @',current_price,' for ', amount)

            sell_ledger(strategy_id,count,current_price,amount,BTC,profit,increase,decrease,time)
            print('--sell ledger made--')
            
            count += 1
            amount = float(100 * A)
            BTC = amount/current_price
            
            buy_ledger(strategy_id,count,current_price,amount,BTC,increase,decrease,time)
            print('--buy ledger made--')
            
            
            


          
  

ws = websocket.WebSocketApp("wss://ws-feed.pro.coinbase.com", on_open=on_open, on_message=on_message)
ws.run_forever()



