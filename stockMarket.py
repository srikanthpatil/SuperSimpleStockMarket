import sqlite3
import math


def load_market_data(stock):
    curr = db.cursor()
    curr.execute(
        f"insert into market_data values ('{stock['symbol']}', '{stock['type']}', {stock['last_dividend']}, {stock['fixedDividend']}, {stock['parValue']} )")
    db.commit()
    curr.close()


def display_market_data():
    curr = db.cursor()
    all_market_data = curr.execute(" SELECT * FROM market_data").fetchall()
    print("************** MARKET DATA *******************\n")
    for stock_data in all_market_data:
        print(stock_data)
    print("**********************************************\n")
    curr.close()


def check_stock_validity(stock):
    curr = db.cursor()
    stock_flag = curr.execute(f" SELECT max(1) FROM market_data where symbol = upper('{stock}')").fetchone()[0]
    curr.close()
    if stock_flag is None:
        print("\n>>>>>>>>> Invalid Stock symbol, please try again with the correct symbol...! <<<<<<<<<<\n")
    return stock_flag


def execute_and_record_trade():
    curr = db.cursor()
    trade_symbol = input("Enter the stock symbol: ")
    trade_type = input("BUY/ SELL?: ")
    trade_quantity = input("Enter the quantity: ")
    trade_price = input("BULL/ SELL price?: ")
    stock_flag = check_stock_validity(trade_symbol)
    if stock_flag is not None:
        max_id = curr.execute(" SELECT max(id) FROM trade_list").fetchone()[0]
        trade_id = 1 if max_id is None else max_id + 1
        print(trade_id)
        curr.execute(
            f"insert into trade_list values ({trade_id}, '{trade_symbol}', '{trade_type}', {trade_quantity}, {trade_price}, datetime('now'))")
        db.commit()
        print(">>>>>>>>> Trade successfully executed...! <<<<<<<<<<")
    curr.close()


def display_trade_data():
    curr = db.cursor()
    all_trade_data = curr.execute(" SELECT * FROM trade_list").fetchall()
    print("*************** TRADE DATA *******************\n")
    for trade_data in all_trade_data:
        print(trade_data)
    print("**********************************************\n")
    curr.close()


def get_dividend_yield(stock, price):
    if check_stock_validity(stock) is not None:
        dividend_rec = db.execute(
            f"select type,last_dividend,fixedDividend, parValue from market_data where symbol = upper('{stock}')").fetchone()
        return dividend_rec[1] / price if dividend_rec[0] == 'Common' else dividend_rec[2] * dividend_rec[3] / price
    return None


def get_pe_ratio(stock, price):
    if check_stock_validity(stock) is not None:
        dividend_yield = get_dividend_yield(stock, price)
        return price / dividend_yield if dividend_yield > 0 else 0
    return None


def get_volume_weighted_stock_price(stock):
    if check_stock_validity(stock) is not None:
        volume_weighted_price = db.execute(
            f"select sum(trade_quantity * trade_price) / sum(trade_quantity) from trade_list where trade_symbol = upper('{stock}') and trade_time >= datetime('Now','-15 minutes')").fetchone()[0]
        return volume_weighted_price
    return None


def get_gbce():
    prices = db.execute("select trade_price from trade_list").fetchall()
    count = 0
    price_product = 1
    for price in prices:
        price_product *= price[0]
        count += 1
    return math.pow(price_product, 1 / count)


def run_stock_market():
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
            execute_and_record_trade()
        elif option == "2":
            stock = input("Enter the Stock Symbol: ")
            price = float(input("Enter the current market price of the Stock: "))
            dividend_yield = get_dividend_yield(stock, price)
            if dividend_yield is not None:
                print(f"Dividend yield for the select stock and the price is : {dividend_yield}")
        elif option == "3":
            stock = input("Enter the Stock Symbol: ")
            price = float(input("Enter the current market price of the Stock: "))
            pe_ratio = get_pe_ratio(stock, price)
            if pe_ratio is not None:
                print(f"PE Ratio for the select stock and the price is : {pe_ratio}")
        elif option == "4":
            stock = input("Enter the Stock Symbol: ")
            volume_weighted_price = get_volume_weighted_stock_price(stock)
            weighted_price = 0 if volume_weighted_price is None else volume_weighted_price
            print(f"Volume weighted price for a selected stock {weighted_price}")
        elif option == "5":
            gbce_index = get_gbce()
            print(f"GBCE All share Index {gbce_index}")
        elif option == "6":
            display_market_data()
        elif option == "7":
            display_trade_data()
        elif option == "0":
            break
        else:
            print(">>>>>>>>> Invalid option selected...! <<<<<<<<<<")


# Stock market data -- Sample data to be loaded on to database
market_data = ({'symbol': 'TEA', 'type': 'Common', 'last_dividend': 0, 'fixedDividend': 0, 'parValue': 100},
               {'symbol': 'POP', 'type': 'Common', 'last_dividend': 8, 'fixedDividend': 0, 'parValue': 100},
               {'symbol': 'ALE', 'type': 'Common', 'last_dividend': 23, 'fixedDividend': 0, 'parValue': 60},
               {'symbol': 'GIN', 'type': 'Preferred', 'last_dividend': 8, 'fixedDividend': 2, 'parValue': 100},
               {'symbol': 'JOE', 'type': 'Common', 'last_dividend': 13, 'fixedDividend': 0, 'parValue': 250})

db = sqlite3.connect("market.s3db")
c = db.cursor()
#c.execute("drop table trade_list")
#db.commit()

# create create a table to hold stock market data if already not there
table_flag = c.execute(" SELECT count(1) FROM sqlite_master WHERE type='table' AND name='market_data' ").fetchone()[0]
if table_flag:
    c.execute("drop table market_data")
c.execute("""create table market_data (symbol TEXT,
type TEXT,
last_dividend INTEGER,
fixedDividend parValue,
parValue parValue)""")
db.commit()
for s in market_data:
    load_market_data(s)

# create create a table to hold the trades executed if already not there
table_flag = c.execute(" SELECT count(1) FROM sqlite_master WHERE type='table' AND name='trade_list' ").fetchone()[0]
if not table_flag:
    c.execute("""create table trade_list (id INTEGER,
    trade_symbol TEXT,
    trade_type TEXT,
    trade_quantity INTEGER,
    trade_price DOUBLE,
    trade_time DATETIME)""")
    db.commit()
c.close()

run_stock_market()
db.close()
