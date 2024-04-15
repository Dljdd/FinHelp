import requests

import asyncio



async def get_art(symbol):
    output = []
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/news/v2/list"

    querystring = {"region":"US","snippetCount":"28","s":symbol}

    payload = " "
    headers = {
        "content-type": "text/plain",
        "X-RapidAPI-Key": "0246fdd8b7mshb7de1e17ea51299p15988ejsn25787ec5a46e",
        "X-RapidAPI-Host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }

    response = requests.post(url, data=payload, headers=headers, params=querystring)

    text = response.json()
    for i in range(10):
        #title
        title = text['data']['main']['stream'][i]['content']['title']
        img = text['data']['main']['stream'][i]['content']['thumbnail']['resolutions'][0]['url']
        # article
        # print(text['data']['main']['stream'][i]['content']['clickThroughUrl']['url'])
        if text['data']['main']['stream'][i]['content']['clickThroughUrl'] is None:
            link = text['data']['main']['stream'][i]['content']['previewUrl']
        else:
            link = text['data']['main']['stream'][i]['content']['clickThroughUrl']['url']
        output.append({"Title": title, "Img_url":img, "Url": link})

    return output

async def get_art_sentiment(symbol):
    op = []
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/news/v2/list"
    querystring = {"region":"US","snippetCount":"28","s":symbol}
    payload = " "
    headers = {
        "content-type": "text/plain",
        "X-RapidAPI-Key": "0246fdd8b7mshb7de1e17ea51299p15988ejsn25787ec5a46e",
        "X-RapidAPI-Host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }
    response = requests.post(url, data=payload, headers=headers, params=querystring)
    text = response.json()
    for i in range(10):
        #title
        title = text['data']['main']['stream'][i]['content']['title']
        # article
        # print(text['data']['main']['stream'][i]['content']['clickThroughUrl']['url'])
        if text['data']['main']['stream'][i]['content']['clickThroughUrl'] is None:
            link = text['data']['main']['stream'][i]['content']['previewUrl']
        else:
            link = text['data']['main']['stream'][i]['content']['clickThroughUrl']['url']
        
        API_URL = "https://api-inference.huggingface.co/models/ProsusAI/finbert"
        headers = {"Authorization": "Bearer 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"}

        def query(payload):
            response = requests.post(API_URL, headers=headers, json=payload)
            return response.json()
            
        output = query({
            "inputs": title,
        })

        if output[0][0]['score'] > output[0][1]['score']:
            if output[0][0]['score'] > output[0][2]['score']:
                score = output[0][0]['score']
                label = output[0][0]['label']
                
        elif output[0][1]['score'] > output[0][2]['score']:
            score = output[0][1]['score']
            label = output[0][1]['label']
        else:
            score =  output[0][2]['score']
            label = output[0][2]['label']
        
        op.append({"Title": title, "Url": link, "Sentiment": label, "Score": score})
    return op
# print(get_art(text))

async def get_stock(symbol, interval, range):
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v3/get-chart"
    
    querystring = {"interval":interval,"symbol":symbol,"range":range,"region":"US","includePrePost":"false","useYfid":"true","includeAdjustedClose":"true","events":"capitalGain,div,split"}

    headers = {
        "X-RapidAPI-Key": "0246fdd8b7mshb7de1e17ea51299p15988ejsn25787ec5a46e",
        "X-RapidAPI-Host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    text = response.json()
    open = text['chart']['result'][0]['indicators']['quote'][0]['open']
    close = text['chart']['result'][0]['indicators']['quote'][0]['close']
    high = text['chart']['result'][0]['indicators']['quote'][0]['high']
    volume = text['chart']['result'][0]['indicators']['quote'][0]['volume']
    low = text['chart']['result'][0]['indicators']['quote'][0]['low']
    timestamp = text['chart']['result'][0]['timestamp']

    # return{"x": timestamp , "y": [open, high, low, close], "volume": volume}
    return {"symbol": symbol, "timestamp": timestamp, "open": open, "high": high, "low": low, "close": close, "volume": volume}


# print(get_stock('AAPL', '1d', '1mo'))