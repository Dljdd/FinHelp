import React, { useState, useEffect } from 'react';
import ReactApexChart from 'react-apexcharts';
import axios from 'axios';
import { useTheme } from '@mui/material/styles';
import Box from '@mui/material/Box';
import MobileStepper from '@mui/material/MobileStepper';
import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import KeyboardArrowLeft from '@mui/icons-material/KeyboardArrowLeft';
import KeyboardArrowRight from '@mui/icons-material/KeyboardArrowRight';
import SwipeableViews from 'react-swipeable-views';
import { autoPlay } from 'react-swipeable-views-utils';
import './Community.css';
import { NewsComponent } from './apidata';
import Navbar from "./Navbar.jsx";

const AutoPlaySwipeableViews = autoPlay(SwipeableViews);

const cryptodata = [
    "BTC-USD",
    "ETH-USD",
    "USDT-USD",
    "BNB-USD",
    "SOL-USD",
    "DOGE-USD",
    "STETH-USD",
    "XRP-USD"
];


export const Crypto = () => {
  const [series, setSeries] = useState([]);
  const [symbol, setSymbol] = useState('AAPL');
  const [interval, setInterval] = useState('1d');
  const [range, setRange] = useState('1mo');
  const theme = useTheme();
  const [activeStep, setActiveStep] = React.useState(0);
  const [images, setImages] = useState([]);

  const handleNext = () => {
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };

  const handleStepChange = (step) => {
    setActiveStep(step);
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const { data } = await axios.post('http://localhost:3010/api/stockdata', { symbol, interval, range });
        const newSeries = [{
          data: data.timestamp.map((timestamp, index) => ({
            x: new Date(timestamp * 1000), // Convert timestamp to milliseconds
            y: [
              parseFloat(data.open[index]).toFixed(3),
              parseFloat(data.high[index]).toFixed(3),
              parseFloat(data.low[index]).toFixed(3),
              parseFloat(data.close[index]).toFixed(3),
            ]
          }))
        }];
        setSeries(newSeries);
        NewsComponent(symbol);
      } catch (error) {
        console.error('Error fetching stock data: ', error);
      }
    };

    fetchData();
  }, [symbol, interval, range]);

  useEffect(() => {
    const fetchImgData = async () => {
      try {
        const { data } = await axios.post('http://localhost:3010/api/news', { symbol });
        setImages(data.map(item => ({
          title: item.Title,
          URL: item.Url,
          image: item.Img_url,
        })));
      } catch (error) {
        console.error('Error fetching stock data: ', error);
      }
    };

    fetchImgData();
  }, [symbol]);

  const options = {
    chart: {
      type: 'candlestick',
      height: 350,
    },
    title: {
      text: 'CandleStick Chart',
      align: 'left',
    },
    xaxis: {
      type: 'datetime',
    },
    yaxis: {
      tooltip: {
        enabled: true,
      },
    },
  };

  return (
    <div>
      <Navbar />
      <div style={{ display: 'flex', justifyContent: 'center', marginBottom: 20 }}>
          <div style={{ marginRight: 20 }}>
            <label htmlFor="symbol">Symbol:</label>
            <select id="symbol" value={symbol} onChange={(e) => setSymbol(e.target.value)}>
              {/* Map through the 'stocks' array and render options dynamically */}
              {cryptodata.map((stock, index) => (
                <option key={index} value={stock}>{stock}</option>
              ))}
            </select>
          </div>
          <div style={{ marginRight: 20 }}>
            <label htmlFor="interval">Interval:</label>
            <select id="interval" value={interval} onChange={(e) => setInterval(e.target.value)}>
              <option value="1d">1d</option>
              <option value="1wk">1wk</option>
              <option value="1mo">1mo</option>
              {/* Add more options as needed */}
            </select>
          </div>
          <div>
            <label htmlFor="range">Range:</label>
            <select id="range" value={range} onChange={(e) => setRange(e.target.value)}>
              <option value="1mo">1mo</option>
              <option value="3mo">3mo</option>
              <option value="6mo">6mo</option>
              {/* Add more options as needed */}
            </select>
          </div>
        </div>
      <div id="chart">
        <ReactApexChart options={options} series={series} type="candlestick" height={350}/>
      </div>
      <div id="html-dist"></div>
    </div>
  );
}

export default Crypto;