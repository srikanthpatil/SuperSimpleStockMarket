from math import pow
from datetime import datetime, timedelta


class Stock:

    def __init__(self, symbol, type, last_dividend, fixed_dividend, par_value):
        self.symbol = symbol
        self.type = type
        self.last_dividend = last_dividend
        self.fixed_dividend = fixed_dividend
        self.par_value = par_value

    def __str__(self):
        return f"Symbol: {self.symbol}, Type: {self.type}, Last Dividend: {self.last_dividend}, Fixed Dividend: {self.fixed_dividend}, Par Value: {self.par_value}"


class Trade:

    def __init__(self, trade_symbol, trade_type, trade_quantity, trade_price):
        self.trade_symbol = trade_symbol
        self.trade_type = trade_type
        self.trade_quantity = trade_quantity
        self.trade_price = trade_price
        self.trade_time = datetime.now()

    def __str__(self):
        return f"Symbol: {self.trade_symbol}, Type: {self.trade_type}, Quantity: {self.trade_quantity}, Price: {self.trade_price}, Time: {self.trade_time}"


class StockMarket:
    trades = []
    market_data = [Stock('TEA', 'Common', 0, 0, 100),
                   Stock('POP', 'Common', 8, 0, 100),
                   Stock('ALE', 'Common', 23, 0, 60),
                   Stock('GIN', 'Preferred', 8, 2, 100),
                   Stock('JOE', 'Common', 13, 0, 250)]

    def check_stock_validity(self, symbol):
        stock = None
        for s in self.market_data:
            if symbol == s.symbol:
                stock = s
        if stock is None:
            print("\n>>>>>>>>> Invalid Stock symbol, please try again with the correct symbol...! <<<<<<<<<<\n")
        return stock

    def execute_and_record_trade(self):
        trade_symbol = input("Enter the stock symbol: ")
        trade_type = input("BUY/ SELL?: ")
        trade_quantity = int(input("Enter the quantity: "))
        trade_price = float(input("BULL/ SELL price?: "))
        if self.check_stock_validity(trade_symbol) is not None:
            self.trades.append(Trade(trade_symbol, trade_type, trade_quantity, trade_price))

    def get_dividend_yield(self, symbol, price):
        stock = self.check_stock_validity(symbol)
        if stock is not None:
            return stock.last_dividend / price if stock.type == 'Common' else stock.fixed_dividend * stock.par_value / price
        return None

    def get_pe_ratio(self, symbol, price):
        if self.check_stock_validity(symbol) is not None:
            dividend_yield = self.get_dividend_yield(symbol, price)
            return price / dividend_yield if dividend_yield > 0 else 0
        return None

    def get_volume_weighted_stock_price(self, symbol):
        if self.check_stock_validity(symbol) is not None:
            numerator = 0
            denominator = 0
            past_time = datetime.now() - timedelta(minutes=15)
            for trade in self.trades:
                if trade.trade_time >= past_time and trade.trade_symbol == symbol:
                    numerator += trade.trade_quantity * trade.trade_price
                    denominator += trade.trade_quantity
            return numerator / denominator if denominator > 0 else 0
        return None

    def get_gbce(self):
        count = 0
        price_product = 1
        for trade in self.trades:
            price_product *= trade.trade_price
            count += 1
        return pow(price_product, 1 / count)

    def display_market_data(self):
        for stock in self.market_data:
            print(stock)

    def display_trade_data(self):
        for trade in self.trades:
            print(trade)

    def run_stock_market(self):
        while True:
            print("\nPlease Choose from the below options...\n")
            print("1. Execute a trade")
            print("2. Calculate Dividend yield")
            print("3. Calculate P/E Ratio")
            print("4. Calculate Volume weighted stock price for the trades in the past 15 minutes")
            print("5. Calculate te GBCE All share Index")
            print("6. Display market data")
            print("7. Display all trades")
            print("0. Exit")
            print(">>")
            option = input()
            if option == "1":
                self.execute_and_record_trade()
            elif option == "2":
                symbol = input("Enter the Stock Symbol: ")
                price = float(input("Enter the current market price of the Stock: "))
                dividend_yield = self.get_dividend_yield(symbol, price)
                if dividend_yield is not None:
                    print(f"Dividend yield for the select stock and the price is : {dividend_yield}")
            elif option == "3":
                symbol = input("Enter the Stock Symbol: ")
                price = float(input("Enter the current market price of the Stock: "))
                pe_ratio = self.get_pe_ratio(symbol, price)
                if pe_ratio is not None:
                    print(f"PE Ratio for the select stock and the price is : {pe_ratio}")
            elif option == "4":
                symbol = input("Enter the Stock Symbol: ")
                volume_weighted_price = self.get_volume_weighted_stock_price(symbol)
                weighted_price = 0 if volume_weighted_price is None else volume_weighted_price
                print(f"Volume weighted price for a selected stock {weighted_price}")
            elif option == "5":
                gbce_index = self.get_gbce()
                print(f"GBCE All share Index {gbce_index}")
            elif option == "6":
                self.display_market_data()
            elif option == "7":
                self.display_trade_data()
            elif option == "0":
                break
            else:
                print(">>>>>>>>> Invalid option selected...! <<<<<<<<<<")


stock_market = StockMarket()
stock_market.run_stock_market()
