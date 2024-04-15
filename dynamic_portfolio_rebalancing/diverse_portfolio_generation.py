import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import warnings
from numba import njit
from collections import defaultdict
import asyncio
import json

from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns, objective_functions

from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices

import vectorbt as vbt

warnings.filterwarnings("ignore")
pd.options.display.float_format = '{:.4f}'.format

def convert_to_native(data):
    if isinstance(data, np.int64):
        return int(data)
    elif isinstance(data, dict):
        return {k: convert_to_native(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_to_native(item) for item in data]
    else:
        return data

crypto_symbols = ['BTC-USD', 'ETH-USD', 'USDT-USD', 'BNB-USD', 'SOL-USD', 'DOGE-USD', 'STETH-USD', 'XRP-USD']

stock_symbols = [ 'JCI', 'TGT', 'CMCSA', 'CPB', 'MO', 'APA', 'MMC', 'JPM',
        'ZION', 'PSA', 'BAX', 'BMY', 'LUV', 'PCAR', 'TXT', 'TMO',
        'DE', 'MSFT', 'HPQ', 'SEE', 'VZ', 'CNP', 'NI', 'T', 'BA','AAPL'] 

mutual_funds_symbols = ['ENPIX', 'ENPSX', 'BIPSX', 'WWNPX', 'KNPCX', 'CSVIX', 'CYPSX', 'ACWIX', 'TIQIX', 'TROCX']


async def api_call(total_investment_amount, asset_allocation = {"stock":0.6,"crypto":0.1,"mf":0.3}, diversity_order = {"stock":10,"crypto":2,"mf":3}):

    investment_stocks = total_investment_amount * asset_allocation["stock"]
    investment_crypto = total_investment_amount * asset_allocation["crypto"]
    investment_mf = total_investment_amount * asset_allocation["mf"]
    # tasks =  [
    #     get_diverse_portfolio(symbols=stock_symbols, investment_amount=investment_stocks, diversity_order=diversity_order["stock"]),
    #     get_diverse_portfolio(symbols=crypto_symbols, investment_amount=investment_crypto, diversity_order=diversity_order["crypto"], year_freq='365'),
    #     get_diverse_portfolio(symbols=mutual_funds_symbols, investment_amount=investment_mf, diversity_order=diversity_order["mf"])
    # ]
    # stock_dict, crypto_dict, mutual_funds_dict = await asyncio.gather(*tasks)
    stock_dict = await get_diverse_portfolio(symbols=stock_symbols, investment_amount=investment_stocks, diversity_order=diversity_order["stock"])
    crypto_dict = await get_diverse_portfolio(symbols=crypto_symbols, investment_amount=investment_crypto, diversity_order=diversity_order["crypto"], year_freq='365')
    mutual_funds_dict = await get_diverse_portfolio(symbols=mutual_funds_symbols, investment_amount=investment_mf, diversity_order=diversity_order["mf"])
    my_dict = {"stocks": stock_dict,"crypto": crypto_dict, "mutual": mutual_funds_dict}
    # Read the dictionary from the file
    val = {k: v.item() if isinstance(v, np.int64) else v for k, v in my_dict.items()}
    # json.dump(val, json_file)
    converted_data = convert_to_native(val)
    json_data = json.dumps(converted_data)

    stock_dict = await get_diverse_portfolio(symbols=stock_symbols, investment_amount=investment_stocks, diversity_order=diversity_order["stock"])
    crypto_dict = await get_diverse_portfolio(symbols=crypto_symbols, investment_amount=investment_crypto, diversity_order=diversity_order["crypto"], year_freq='365')
    mutual_funds_dict = await get_diverse_portfolio(symbols=mutual_funds_symbols, investment_amount=investment_mf, diversity_order=diversity_order["mf"])

    print(stock_dict)

    my_dict = {"stocks": stock_dict,"crypto": crypto_dict, "mutual": mutual_funds_dict}

    val = {k: v.item() if isinstance(v, np.int64) else v for k, v in my_dict.items()}

    converted_data = convert_to_native(val)
    json_data = json.dumps(converted_data)

    return json_data

async def get_diverse_portfolio(symbols, investment_amount, max_risk_threshold = 1.0, max_return_threshold = 0.1, diversity_order = 1, year_freq = '252'):
    symbols.sort()
    start_date = '2020-01-01'
    end_date = '2023-01-01'

    vbt.settings.array_wrapper['freq'] = 'days'
    vbt.settings.returns['year_freq'] = year_freq
    vbt.settings.portfolio.stats['incl_unrealized'] = True

    yfdata = vbt.YFData.download(symbols, start=start_date, end=end_date)

    ohlcv = yfdata.concat()

    close_price = ohlcv['Close']
    open_price = ohlcv['Open']

    features = [close_price, open_price]
    feature_list = ["close_price", "open_price"]

    output_dict = {
        "close_price" : {1: [], 2: [], 3: []},
        "open_price" : {1: [], 2: [], 3: []},
    }

    for index,feature in enumerate(features):
        avg_returns = expected_returns.mean_historical_return(feature, frequency=int(year_freq))
        cov_mat = risk_models.sample_cov(feature, frequency=int(year_freq))

        allocation_sh, value_counts_sh, return_stats_sh, port_performance_sh = await max_sharpe_score(symbols, avg_returns, cov_mat, feature, investment_amount, diversity_order)
        allocation_ret, value_counts_ret, return_stats_ret, port_performance_ret = await max_efficient_return(symbols, avg_returns, cov_mat, feature, investment_amount, diversity_order, max_return_threshold)
        allocation_risk, value_counts_risk, return_stats_risk, port_performance_risk = await max_efficient_risk(symbols, avg_returns, cov_mat, feature, investment_amount, diversity_order, max_risk_threshold)

        output_dict[feature_list[index]][1].extend([allocation_sh, value_counts_sh, return_stats_sh, port_performance_sh])
        output_dict[feature_list[index]][2].extend([allocation_ret, value_counts_ret, return_stats_ret, port_performance_ret])
        output_dict[feature_list[index]][3].extend([allocation_risk, value_counts_risk, return_stats_risk, port_performance_risk])
    return output_dict

async def max_sharpe_score(symbols, avg_returns, cov_mat, feature, investment_amount, diversity_order):

    gamma = 0.01
    curr_div_order = 0 

    while curr_div_order < diversity_order:

        ef = EfficientFrontier(avg_returns, cov_mat)
        ef.add_objective(objective_functions.L2_reg, gamma = gamma)

        weights = ef.max_sharpe()

        portfolio_performance = ef.portfolio_performance()

        clean_weights = ef.clean_weights()

        pyopt_weights = np.array([clean_weights[symbol] for symbol in symbols])

        latest_prices = get_latest_prices(feature)

        da = DiscreteAllocation(weights, latest_prices, total_portfolio_value=investment_amount)

        allocation, leftover = da.lp_portfolio()

        pyopt_size = np.zeros_like(feature)
        pyopt_size[0, :] = pyopt_weights  # allocate at first timestamp, do nothing afterwards

        # Run simulation with weights from PyPortfolioOpt
        pyopt_pf = vbt.Portfolio.from_orders(
            close=feature,
            size=pyopt_size,
            size_type='targetpercent',
            group_by=True,
            cash_sharing=True
        )

        curr_div_order = len(pyopt_pf.orders)

        if curr_div_order < diversity_order:
            gamma = gamma + 0.5
            del ef

    value_counts = {"Count" : sum(allocation.values())}

    portfolio_performance_dict = {
        "Expected annual return [%]" : portfolio_performance[0],
        "Annual volatility [%]" : portfolio_performance[1]
    }

    stats_dict = {
    'Start': '2014-09-17 00:00:00',
    'End': '2022-12-31 00:00:00',
    'Period': str(pyopt_pf.stats().loc['Period']),
    'Start Value': pyopt_pf.stats().loc['Start Value'],
    'End Value': pyopt_pf.stats().loc['End Value'],
    'Total Return [%]': pyopt_pf.stats().loc['Total Return [%]'],
    'Benchmark Return [%]': pyopt_pf.stats().loc['Benchmark Return [%]'],
    'Sharpe Ratio': pyopt_pf.stats().loc['Sharpe Ratio'],
    }

    return allocation, value_counts, stats_dict, portfolio_performance_dict

async def max_efficient_return(symbols, avg_returns, cov_mat, feature, investment_amount, diversity_order, max_return_threshold):
    gamma = 0.01
    curr_div_order = 0 

    while curr_div_order < diversity_order:

        ef = EfficientFrontier(avg_returns, cov_mat)
        ef.add_objective(objective_functions.L2_reg, gamma = gamma)

        weights = ef.efficient_return(target_return=max_return_threshold)

        portfolio_performance = ef.portfolio_performance()

        clean_weights = ef.clean_weights()

        pyopt_weights = np.array([clean_weights[symbol] for symbol in symbols])

        latest_prices = get_latest_prices(feature)

        da = DiscreteAllocation(weights, latest_prices, total_portfolio_value=investment_amount)

        allocation, leftover = da.lp_portfolio()

        pyopt_size = np.zeros_like(feature)
        pyopt_size[0, :] = pyopt_weights  # allocate at first timestamp, do nothing afterwards

        # Run simulation with weights from PyPortfolioOpt
        pyopt_pf = vbt.Portfolio.from_orders(
            close=feature,
            size=pyopt_size,
            size_type='targetpercent',
            group_by=True,
            cash_sharing=True
        )

        curr_div_order = len(pyopt_pf.orders)

        if curr_div_order < diversity_order:
            gamma = gamma + 0.5
            del ef

    value_counts = {"Count" : sum(allocation.values())}

    portfolio_performance_dict = {
        "Expected annual return [%]" : portfolio_performance[0],
        "Annual volatility [%]" : portfolio_performance[1]
    }

    stats_dict = {
    'Start': '2014-09-17 00:00:00',
    'End': '2022-12-31 00:00:00',
    'Period': str(pyopt_pf.stats().loc['Period']),
    'Start Value': pyopt_pf.stats().loc['Start Value'],
    'End Value': pyopt_pf.stats().loc['End Value'],
    'Total Return [%]': pyopt_pf.stats().loc['Total Return [%]'],
    'Benchmark Return [%]': pyopt_pf.stats().loc['Benchmark Return [%]'],
    'Sharpe Ratio': pyopt_pf.stats().loc['Sharpe Ratio'],
    }

    return allocation, value_counts, stats_dict, portfolio_performance_dict

async def max_efficient_risk(symbols, avg_returns, cov_mat, feature, investment_amount, diversity_order, max_risk_threshold):
    gamma = 0.01
    curr_div_order = 0 

    while curr_div_order < diversity_order:

        ef = EfficientFrontier(avg_returns, cov_mat)
        ef.add_objective(objective_functions.L2_reg, gamma = gamma)

        weights = ef.efficient_risk(target_volatility=max_risk_threshold)

        portfolio_performance = ef.portfolio_performance()

        clean_weights = ef.clean_weights()

        pyopt_weights = np.array([clean_weights[symbol] for symbol in symbols])

        latest_prices = get_latest_prices(feature)

        da = DiscreteAllocation(weights, latest_prices, total_portfolio_value=investment_amount)

        allocation, leftover = da.lp_portfolio()

        pyopt_size = np.zeros_like(feature)
        pyopt_size[0, :] = pyopt_weights  # allocate at first timestamp, do nothing afterwards

        # Run simulation with weights from PyPortfolioOpt
        pyopt_pf = vbt.Portfolio.from_orders(
            close=feature,
            size=pyopt_size,
            size_type='targetpercent',
            group_by=True,
            cash_sharing=True
        )

        curr_div_order = len(pyopt_pf.orders)

        if curr_div_order < diversity_order:
            gamma = gamma + 0.5
            del ef

    value_counts = {"Count" : sum(allocation.values())}

    portfolio_performance_dict = {
        "Expected annual return [%]" : portfolio_performance[0],
        "Annual volatility [%]" : portfolio_performance[1]
    }

    stats_dict = {
    'Start': '2014-09-17 00:00:00',
    'End': '2022-12-31 00:00:00',
    'Period': str(pyopt_pf.stats().loc['Period']),
    'Start Value': pyopt_pf.stats().loc['Start Value'],
    'End Value': pyopt_pf.stats().loc['End Value'],
    'Total Return [%]': pyopt_pf.stats().loc['Total Return [%]'],
    'Benchmark Return [%]': pyopt_pf.stats().loc['Benchmark Return [%]'],
    'Sharpe Ratio': pyopt_pf.stats().loc['Sharpe Ratio'],
    }

    return allocation, value_counts, stats_dict, portfolio_performance_dict

def convert_to_native(data):
    if isinstance(data, np.int32):
        return int(data)
    elif isinstance(data, dict):
        return {k: convert_to_native(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_to_native(item) for item in data]
    else:
        return data

async def rebalancing(total_investment_amount, stage_1 = False, asset_allocation = {"stock":0.6,"crypto":0.1,"mf":0.3}, diversity_order = {"stock":10,"crypto":2,"mf":3}):
    if stage_1 is False:
        metric, strategy = await get_user_strategy()
        investment_stocks = total_investment_amount * asset_allocation["stock"]
        investment_crypto = total_investment_amount * asset_allocation["crypto"]
        investment_mf = total_investment_amount * asset_allocation["mf"]

        allocation_st, value_counts_st, _n, _n = stage_1(metric = metric, strategy = strategy, symbols = stock_symbols, investment_amount = investment_stocks, max_risk_threshold = 1.0, max_return_threshold = 0.1, diversity_order = diversity_order["stock"])
        allocation_cr, value_counts_cr, _n, _n = stage_1(metric = metric, strategy = strategy, symbols = crypto_symbols, investment_amount = investment_crypto, max_risk_threshold = 1.0, max_return_threshold = 0.1, diversity_order = diversity_order["crypto"], year_freq = '365')
        allocation_mf, value_counts_mf, _n, _n = stage_1(metric = metric, strategy = strategy, symbols = mutual_funds_symbols, investment_amount = investment_mf, max_risk_threshold = 1.0, max_return_threshold = 0.1, diversity_order = diversity_order["mf"])

        value_counts_dict = {"stock" : value_counts_st['Count'], 
                            "crypto" : value_counts_cr['Count'], 
                            "mf" : value_counts_mf['Count']}
        
        value_ratios_dict = {key: value / sum(value_counts_dict.values()) for key, value in value_counts_dict.items()}
        user_dict = {**allocation_st, **allocation_cr, **allocation_mf}

        with open('value_ratios_dict.json', 'w') as json_file:
            json.dump(value_ratios_dict, json_file)
            
        with open('user_dict.json', 'w') as json_file:
            json.dump(user_dict, json_file)

        await save_date()

    else:
        metric, strategy = await get_user_strategy()
        total_investment_amount = await calc_capital()

        with open('value_ratios_dict.json', 'r') as json_file:
            value_ratios_dict = json.load(json_file)
        
        investment_stocks = total_investment_amount * asset_allocation["stock"]
        investment_crypto = total_investment_amount * asset_allocation["crypto"]
        investment_mf = total_investment_amount * asset_allocation["mf"]

        allocation_st, value_counts_st, _n, _n = stage_1(metric = metric, strategy = strategy, symbols = stock_symbols, investment_amount = investment_stocks, max_risk_threshold = 1.0, max_return_threshold = 0.1, diversity_order = diversity_order["stock"])
        allocation_cr, value_counts_cr, _n, _n = stage_1(metric = metric, strategy = strategy, symbols = crypto_symbols, investment_amount = investment_crypto, max_risk_threshold = 1.0, max_return_threshold = 0.1, diversity_order = diversity_order["crypto"], year_freq = '365')
        allocation_mf, value_counts_mf, _n, _n = stage_1(metric = metric, strategy = strategy, symbols = mutual_funds_symbols, investment_amount = investment_mf, max_risk_threshold = 1.0, max_return_threshold = 0.1, diversity_order = diversity_order["mf"])

        with open('user_dict.json', 'r') as json_file:
            user_dict_old = json.load(json_file)
        
        user_dict_new = {**allocation_st, **allocation_cr, **allocation_mf}

        sell_trades, buy_trades = await get_trades(user_dict_old, user_dict_new)

        with open('user_dict.json', 'w') as json_file:
            json.dump(user_dict_new, json_file)
  
        value_counts_dict = {"stock" : value_counts_st['Count'], 
                            "crypto" : value_counts_cr['Count'], 
                            "mf" : value_counts_mf['Count']}
        
        value_ratios_dict = {key: value / sum(value_counts_dict.values()) for key, value in value_counts_dict.items()}
        
        with open('value_ratios_dict.json', 'w') as json_file:
            json.dump(value_ratios_dict, json_file)

        await save_date()

        return sell_trades, buy_trades
    
async def save_date():
    stored_date = datetime.now().date()
    with open('stored_date.txt', 'w') as f:
        f.write(stored_date.strftime('%Y-%m-%d'))
    pass

async def check_days(total_investment_amount, n_days = 30):
    try:
        with open('stored_date.txt', 'r') as f:
            stored_date_str = f.read()
            stored_date = datetime.strptime(stored_date_str, '%Y-%m-%d')

            current_date = datetime.now()

            if (current_date - stored_date).days >= n_days:
                await rebalancing(total_investment_amount = total_investment_amount, stage_1=True)

    except FileNotFoundError:
        stored_date = None
        pass

async def get_user_strategy():
    user_choices = {
        "metric" : "Close",
        "strategy" : "Sharpe"
    }

    return user_choices['metric'], user_choices['strategy']

async def stage_1(metric, strategy, symbols, investment_amount, max_risk_threshold = 1.0, max_return_threshold = 0.1, diversity_order = 1, year_freq = '252'):
    symbols.sort()
    start_date = '2020-01-01'
    end_date = '2023-01-01'

    vbt.settings.array_wrapper['freq'] = 'days'
    vbt.settings.returns['year_freq'] = year_freq
    vbt.settings.portfolio.stats['incl_unrealized'] = True

    yfdata = vbt.YFData.download(symbols, start=start_date, end=end_date)

    ohlcv = yfdata.concat()

    if metric == "close":
        feature_list = 'close_price'
        price = ohlcv['Close']
    else:
        feature_list = 'open_price'
        price = ohlcv['Open'] 

    avg_returns = expected_returns.mean_historical_return(price, frequency=int(year_freq))
    cov_mat = risk_models.sample_cov(price, frequency=int(year_freq))

    if strategy == 'Sharpe':
        return await max_sharpe_score(symbols = symbols, avg_returns = avg_returns, cov_mat = cov_mat, price = price, investment_amount = investment_amount, diversity_order = diversity_order)

    elif strategy == 'Max Return':
       return await max_efficient_return(symbols, avg_returns, cov_mat, price, investment_amount, diversity_order, max_return_threshold)

    else:
       return await max_efficient_risk(symbols, avg_returns, cov_mat, price, investment_amount, diversity_order, max_risk_threshold)

async def calc_capital(metric):
    end_date = datetime.now().strftime('%Y-%m-%d')
    days_back = 1

    # Calculate the start date by subtracting days_back from the end date
    start_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')

    # Download data
    yfdata_st = vbt.YFData.download(symbols= stock_symbols, start=start_date, end=end_date)
    yfdata_cr = vbt.YFData.download(symbols= crypto_symbols, start=start_date, end=end_date)
    yfdata_mf = vbt.YFData.download(symbols= mutual_funds_symbols, start=start_date, end=end_date)

    # Concatenate data
    ohlcv_st = yfdata_st.concat()
    ohlcv_cr = yfdata_cr.concat()
    ohlcv_mf = yfdata_mf.concat()

    if metric == "close":
        feature_list = 'close_price'
        price_st = ohlcv_st['Close']
        price_cr = ohlcv_cr['Close']
        price_mf = ohlcv_mf['Close']
    else:
        feature_list = 'open_price'
        price_st = ohlcv_st['Opem']
        price_cr = ohlcv_cr['Open']
        price_mf = ohlcv_mf['Open']

    price_st_np = price_st.to_numpy()
    price_cr_np = price_cr.to_numpy()
    price_mf_np = price_mf.to_numpy()

    # Combine them into one numpy array along the second axis (axis=1 for columns)
    combined_prices = np.concatenate((price_st_np, price_cr_np, price_mf_np), axis=1)

    with open('user_dict.json', 'r') as json_file:
        user_dict = json.load(json_file)

    values_array = np.array(list(user_dict.values()))

    return np.dot(values_array, combined_prices)

async def get_trades(user_dict_old, user_dict_new):
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

import asyncio

asyncio.run(api_call(20000))
