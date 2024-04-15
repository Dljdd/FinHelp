const express = require('express');
const cors = require('cors');
const axios = require('axios');

const app = express();
const PORT = 3010;

app.use(express.json()); // Middleware to parse JSON requests
app.use(cors()); // Enable CORS for all routes

async function fetchnews(symbol) {
  const url = "https://fin-api-9thj.onrender.com/get_article";

  const requestBody = {
    symbol: symbol
  };

  try {
    const response = await axios.post(url, requestBody);
    const data = response.data;
    console.log(data);
    return data;
  } catch (error) {
    console.error('Error fetching news: ', error);
  }
}

async function fetchStockData(symbol, interval, range) {
  const url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v3/get-chart";

  const querystring = {
    interval: interval,
    symbol: symbol,
    range: range,
    region: "US",
    includePrePost: "false",
    useYfid: "true",
    includeAdjustedClose: "true",
    events: "capitalGain,div,split"
  };

  const headers = {
    "X-RapidAPI-Key": "0246fdd8b7mshb7de1e17ea51299p15988ejsn25787ec5a46e",
    "X-RapidAPI-Host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
  };

  try {
    const response = await axios.get(url, { headers: headers, params: querystring });
    const data = response.data;
    const open = data.chart.result[0].indicators.quote[0].open;
    const close = data.chart.result[0].indicators.quote[0].close;
    const high = data.chart.result[0].indicators.quote[0].high;
    const volume = data.chart.result[0].indicators.quote[0].volume;
    const low = data.chart.result[0].indicators.quote[0].low;
    const timestamp = data.chart.result[0].timestamp;
    console.log({symbol: symbol,
      timestamp: timestamp,
      open: open,
      high: high,
      low: low,
      close: close,
      volume: volume});
    return {
      symbol: symbol,
      timestamp: timestamp,
      open: open,
      high: high,
      low: low,
      close: close,
      volume: volume
    };
  } catch (error) {
    console.error('Error fetching stock ', error);
    throw error; // Rethrow the error to be caught by the caller
  }
}

app.post('/api/stockdata', async (req, res) => {
  const symbol = req.body.symbol;
  const interval = req.body.interval;
  const range = req.body.range;

  try {
    const stockData = await fetchStockData(symbol, interval, range);
    res.json(stockData); // Send the fetched data as JSON response
  } catch (error) {
    console.error('Error fetching stock data: ', error);
    res.status(500).send('Internal Server Error');
  }
});

app.post('/api/news', async (req, res) => {
  const symbol = req.body.symbol;
  try {
    const response = await fetchnews(symbol);
    res.json(response); // Send the fetched data as JSON response
    console.log(response);
  } catch (error) {
    console.error('Error fetching stock data: ', error);
    res.status(500).send('Internal Server Error');
  }
});

app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});

