#import robin_stocks as robin
from robin_stocks import robinhood as rs
import time, json
import pandas as pd
from authentication import login, logout

class Robin:
    def __init__(self):
        self.name = rs

    # Added the =self part to make sure that I'm signing out.
    def signIn(self):
        logins = self.loadJson()
        log = login(username=logins["user_name"], password=logins["password"], expiresIn=23500)
        return log
    
    def loadJson(self):
        with open("login.json", "r") as statusFile:
            me = json.load(statusFile)
            statusFile.close()
            return me
    #
    def signOut(self):
        logout()
    #
    def buyingPower(self):
        return float(self.name.profiles.load_account_profile()["buying_power"])
    #
    def buyOrder(self, name, amount, extended):
        return self.name.orders.order_buy_fractional_by_quantity(name, amount, timeInForce='gtc', extendedHours=extended)
    #
    def limitOrder(self, name, quantity, limitPrice, extended):
        return self.name.orders.order_buy_limit(name, quantity, limitPrice, timeInForce='gtc', extendedHours=extended)
    #
    def buyCrypto(self, name, dollarAmount):
        return self.name.orders.order_buy_crypto_by_price(name, dollarAmount, timeInForce='gtc', jsonify=True)
        
    #
    def sellCrypto(self, name, quantity, limitPrice):
        return self.name.orders.order_crypto(name, "sell", quantity, limitPrice, timeInForce='gtc', jsonify=True)
         
    #
    def sell_limit_Crypto(self, name, quantity, limitPrice):
        return self.name.orders.order_sell_crypto_limit(name, quantity, limitPrice, timeInForce='gtc', jsonify=True)   
    #
    def CryptoLimitOrder(self, name, quantity, price):
        return self.name.orders.order_buy_crypto_limit(name, quantity, price, timeInForce='gtc', jsonify=True)  
    # example: optionLimit('open', 250, JKS, 10, '2021-03-13', 70, 'call')
    def optionLimit(self, action, price, name, quantity, expiration, strike, optionType):
        return self.name.orders.order_buy_option(action, 'debut', price, name, quantity, expiration, strike, optionType=optionType, timeInForce='gtc')    
    # name can be a single name or a list of names.
    def getLatestPrice(self, name):
        s = self.name.stocks.get_latest_price(name, includeExtendedHours=True)
        if s[0]:
            return float(s[0])
        return -1
    # This waits until the price of a stock goes below the target price to get triggered. 
    def buyAt(self, name, targetPrice, amount):
        while True:
            try:
                price = self.getLatestPrice(name)
                if price <= targetPrice:
                    try:
                        s = self.buyOrder(self, name, amount, False)
                        #return s  
                        break
                    except Exception as e:
                        print(f"Error placing order: {e}") 
                else:
                    time.sleep(15)
            except Exception as e:
                print(f"Error fetching the latest price : {e}")
        print(f"ORDER TRIGGERED AT {pd.Timestamp.now()}")
    #
    def getCryptoPrice(self, name):
        return float(self.name.crypto.get_crypto_quote(name)['mark_price'])
    # this function waits for the stock to go down one percent and then buys, and sells at 1 positive.
    def percentBuyStock(self):
        df = pd.DataFrame(columns=['date', 'price'])
        while True:
            try:
                price = self.name.stocks.get_latest_price('MA', includeExtendedHours=True)
                # assigning price to first (and only) item of list and converting from str to float
                mastercard_price = float(price[0])
                
                df.loc[len(df)] = [pd.Timestamp.now(), mastercard_price]
                
                start_time = df.date.iloc[-1] - pd.Timedelta(minutes=60)
                df = df.loc[df.date >= start_time] # cuts dataframe to only include last hour of data
                max_price = df.price.max()
                min_price = df.price.min()
                
                if df.price.iloc[-1] < max_price * 0.99:
                    try:
                        self.name.orders.order_buy_fractional_by_price('V', 10)
                        print("DROPPED 1%, CURRENT PRICE: {} MAX PRICE: {}".format(df.price.iloc[-1], max_price))
                        break
                        
                    except Exception as e:
                        print("Error placing order:", e)
                        
                elif df.price.iloc[-1] > min_price * 1.01:
                    try:
                        self.name.orders.order_sell_fractional_by_price('V', 10)
                        print("RISEN 1%, CURRENT PRICE: {} MIN PRICE: {}".format(df.price.iloc[-1], min_price))
                        break
                        
                    except Exception as e:
                        print("Error placing order:", e)
                
                else:
                    print("NO ORDER, CURRENT PRICE: {} MIN PRICE: {} MAX PRICE: {}\n".format(df.price.iloc[-1], min_price, max_price))
                    time.sleep(15)
                        
            except Exception as e:
                print("Error fetching latest price:", e)
            
        print("ORDER TRIGGERED at {}".format(pd.Timestamp.now()))
    
        # firing a pair trade when Dropbox and box diverge more than 3% over the previous day FULL EXAMPLE

        dropbox_data = self.name.stocks.get_stock_historicals("DBX", interval="day", span="week")
        dropbox_historical = pd.DataFrame(dropbox_data)

        box_data = self.name.stocks.get_stock_historicals("BOX", interval="day", span="week")
        box_historical = pd.DataFrame(box_data)

        price_diff_yesterday = dropbox_historical.iloc[-1]['close_price'] - box_historical.iloc[-1]['close_price']

        while True:
            try:
                dropbox_today = float(self.name.stocks.get_latest_price('DBX', includeExtendedHours=True)[0])
                box_today = float(self.name.stocks.get_latest_price('BOX', includeExtendedHours=True)[0])
                print("box today:", box_today)
                print("dropbox today:", dropbox_today)

                price_diff_today = dropbox_today - box_today

                if price_diff_today > 1.03 * price_diff_yesterday:
                    try:
                        # LONG BOX SHORT DROPBOX
                        self.name.orders.order_buy_fractional_by_price('BOX',
                                                500,
                                                timeInForce='gtc',
                                                extendedHours=False) 

                        self.name.orders.order_sell_fractional_by_price('DBX',            
                                                500,
                                                timeInForce='gtc',
                                                extendedHours=False) 

                        print("Diverged MORE THAN 3%, YESTERDAY'S DIFFERENCE: {} TODAY'S DIFFERENCE: {} PERCENTAGE CHANGE: {}%\n".format(price_diff_yesterday, price_diff_today, (price_diff_today/price_diff_yesterday - 1)*100))
                        break
                    except Exception as e:
                        print("Error placing orders:", e)
                        time.sleep(15)

                else:
                    print("STILL WAITING, YESTERDAY'S DIFFERENCE: {} TODAY'S DIFFERENCE: {} PERCENTAGE CHANGE: {}%\n".format(price_diff_yesterday, price_diff_today, ((price_diff_today/price_diff_yesterday - 1))*100))
                    time.sleep(15)
            except Exception as e:
                print("Error fetching latest prices:", e)
                time.sleep(15)

        print("ORDER TRIGGERED at {}".format(pd.Timestamp.now()))
    
    def percentBuyOption(self, name):
        df = pd.DataFrame(columns=['date', 'price'])
        while True:
            try:
                price = self.name.stocks.get_latest_price('TSLA', includeExtendedHours=True)
                # assigning price to first (and only) item of list and converting from str to float
                tesla_price = float(price[0])
                
                df.loc[len(df)] = [pd.Timestamp.now(), tesla_price]
                
                start_time = df.date.iloc[-1] - pd.Timedelta(minutes=60)
                df = df.loc[df.date >= start_time] # cuts dataframe to only include last hour of data
                max_price = df.price.max()
                min_price = df.price.min()
                
                if (df.price.iloc[-1] < max_price * 0.99 or df.price.iloc[-1] > min_price * 1.01):
                    try:
                        # finds current best bid for option contract we want to buy
                        best_bid = self.name.options.find_options_by_expiration_and_strike('TSLA',
                                                                        '2020-07-17',
                                                                        1580,
                                                                        optionType='call',
                                                                        info='bid_price')
                        # converts output to float
                        best_bid = float(best_bid[0])
                        # we place our limit bid 0.1% above the current best bid
                        our_bid = 1.001 * best_bid
                        
                        self.name.orders.order_buy_option_limit('open', 
                                        'debit', 
                                        our_bid, 
                                        'TSLA',
                                        1,
                                        '2020-07-17', 
                                        1580, 
                                        optionType='call', 
                                        timeInForce='gtc')
                        print("MOVED MORE THAN 1%, TESLA CURRENT PRICE: {} MIN PRICE: {} MAX PRICE: {}\n".format(df.price.iloc[-1], min_price, max_price))
                        break
                        
                    except Exception as e:
                        print("Error placing order:", e)
                
                else:
                    print("NO ORDER, TESLA CURRENT PRICE: {} MIN PRICE: {} MAX PRICE: {}\n".format(df.price.iloc[-1], min_price, max_price))
                    time.sleep(15)
                        
            except Exception as e:
                print("Error fetching latest price:", e)
                
        print("ORDER TRIGGERED at {}".format(pd.Timestamp.now()))
        print("LIMIT BUY FOR OPTION CALL PLACED AT:", our_bid)
    # date format : '2020-07-17'
    def getTheGreeks(self, name, date, opType, strikePrice):
        delta = float(self.name.options.get_option_market_data(name,
                                                date,
                                                strikePrice,
                                                optionType=opType,
                                                info='delta')[0])
    #
    def getAccountStatus(self):
        s = self.name.account.get_all_positions()
        print(f"Status is : {s}")
        return s
    # Gets all of the open orders that I have.
    def getOpenOrders(self):
        cryptoOpenOrders = self.name.orders.get_all_open_crypto_orders()
        optionOpenOrders = self.name.orders.get_all_open_option_orders()
        stockOpenOrders = self.name.orders.get_all_open_stock_orders()
        print(f"Crypto: {cryptoOpenOrders}\nOptions: {optionOpenOrders}\nStock: {stockOpenOrders}")
        return [cryptoOpenOrders, optionOpenOrders, stockOpenOrders]
    # Returns a list of dictionaries of key/value pairs for each crypto.
    def getMyCryptos(self):
        return self.name.crypto.get_crypto_positions()
    # Returns a list of dictionaries of key/value pairs for each option.
    def getMyOptions(self):
        return self.name.options.get_open_option_positions()
    # Returns a list of dictionaries of key/value pairs for each ticker.
    def getMyStocks(self):
        return self.name.account.get_open_stock_positions()
    # calcels all orders of the type t
    def cancelOpenOrders(self, t):
        if t == 'crypto':
            cryptoOpenOrders = self.name.orders.cancel_all_crypto_orders()
        elif t == 'option':
            optionOpenOrders = self.name.orders.cancel_all_option_orders()
        elif t == 'stock':
            stockOpenOrders = self.name.orders.cancel_all_stock_orders()
        else:
            print(f"Error wrong argument: {t}")
    # cancels an order based on the type
    def cancel_order(self, t, id):
        if t == 'crypto':
            cryptoOpenOrders = self.name.orders.cancel_crypto_order(id)
        elif t == 'option':
            optionOpenOrders = self.name.orders.cancel_option_order(id)
        elif t == 'stock':
            stockOpenOrders = self.name.orders.cancel_stock_order(id)
        else:
            print(f"Error wrong argument: {t}")
    # collects option data for a give stock name.
    def getOptionData(self, name, date, price, opType, inter, span):
        tesla_data = self.name.stocks.get_options_historicals(name, date, price, opType, interval=inter+"minute", span=span)
        tesla_dataframe = pd.DataFrame(tesla_data)
        print(tesla_data)
    # gets the valid exp dates for a stock.
    def getExpiration(self, name, info):
        s = self.name.options.get_chains("AAPL", info='expiration_dates')
        return s
    # get basic info for a stock.
    def getFundamental(self, name):
        s = self.name.stocks.get_fundamentals(name, info=None)
        print(s)
        return s    
    # saves both stock and option complete orders.
    def saveStockData(self, name):
        stock = self.name.export.export_completed_stock_orders("order_history", "stocks_monday")
        option = self.name.export.export_completed_option_orders("order_history", "options_monday")
    #
    def collectData(self, lst):
        result = []
        for name in lst:
            price = float(self.getLatestPrice([name]))
            result.append(price)
        return result
    #
    def dayData(self, names=[]):
        t = 0
        while t < 78:
            prices = self.collectData(names)
            for index in range(len(names)):
                if t == (78 - 1):
                    self.append(names[index], (str(prices[index]) + "\n"))
                    return True
                else:
                    self.append(names[index], (str(prices[index]) + " "))
            t += 1
            time.sleep(300)
        return "Done"
    #
    def append(self, name, data):
        f = open(name, 'a')
        f.write(data)
        f.close()
    #
    def runner(self):
        stocks = ["AAPL", "TSLA", "PLTR", "ACB", "TLRY", "RTX", "BA", "NFLX", "SPY", "FSLY", "JKS", "PLUG"]
        day = time.strftime('%A')
        week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        i = 0
        while (day in week):
                print(f"Getting data for day {i}")
                for n in stocks:
                    self.append(n, "\n"+day+" : ")
                state = self.dayData(stocks)
                print("Data for day [", day, "] is : ", state)
                
                self.signOut(self)
                if day == "Friday":
                    time.sleep(235800)
                else:
                    time.sleep(61200)
                self.signIn(self)
                day = time.strftime('%A')
                i += 1
            
#
if __name__=="__main__":
    myRobin = Robin()
    print(myRobin.getLatestPrice("AAPL"))
    
    myRobin.signOut()
    