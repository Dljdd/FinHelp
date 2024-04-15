def get_trades(user_dict_old, user_dict_new):
    sell_trades = {}
    buy_trades = {}

    for asset, shares_old in user_dict_old.items():
        if asset in user_dict_new:
            shares_new = user_dict_new[asset]
            trade = shares_new - shares_old
            if trade < 0:
                sell_trades[asset] = -trade
            elif trade > 0:
                buy_trades[asset] = trade
        else:
            sell_trades[asset] = -shares_old

    for asset, shares_new in user_dict_new.items():
        if asset not in user_dict_old:
            buy_trades[asset] = shares_new

    return sell_trades, buy_trades

# Example usage:
user_dict_old = {'AAPL': 10, 'GOOGL': 5, 'TSLA': 8}
user_dict_new = {'AAPL': 12, 'MSFT': 6, 'TSLA': 7}

sell_trades, buy_trades = get_trades(user_dict_old, user_dict_new)

print("Sell Trades:", sell_trades)
print("Buy Trades:", buy_trades)
