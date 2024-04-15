import axios from 'axios';

export async function StockDataComponent(symbol, interval, range) {
  try {
    const response = await axios.post('http://localhost:3010/api/stockdata', { symbol, interval, range });
    console.log(response.data.open,response.data.high,response.data.low,response.data.close,response.data.volume,response.data.timestamp);
    return response.data;
  } catch (error) {
    console.error('Error fetching stock data: ', error);
    throw error; // Rethrow the error to be caught by the caller
  }
}

export async function NewsComponent(symbol) {
  try {
    const response = await axios.post('http://localhost:3010/api/news', {symbol});
    console.log(response.data.length);
    console.log(response.data);
    return response.data;
  } catch (error) {
    console.error('Error fetching news data: ', error);
    throw error; 
  }
}