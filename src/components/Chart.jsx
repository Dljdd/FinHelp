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

const stocks = [
  'AAPL',
  'HDFCBANK.BO',
  'RELIANCE.BO',
  'TCS.BO',
  'INFY.BO',
  'TSLA',
  'ICICIBANK.BO',
  'KOTAKBANK.BO',
  'BHARTIARTL.BO',
  'AXISBANK.BO',
  'LT.BO',
  'SBIN.BO',
  'MARUTI.BO',
  'NVDA',
  'HUL.BO',
  'INDUSINDBK.BO',
  'HDFC.BO',
  'BAJFINANCE.BO',
  'WIPRO.BO',
  'ASIANPAINT.BO',
  'TECHM.BO',
  'NESTLEIND.BO',
  'BAJAJFINSV.BO',
  'BAJAJ-AUTO.BO',
  'TITAN.BO',
  'UPL.BO',
  'SHREECEM.BO',
  'DIVISLAB.BO',
  'HDFCBANK.NS',
  'RELIANCE.NS',
  'TCS.NS',
  'INFY.NS',
  'ICICIBANK.NS',
  'KOTAKBANK.NS',
  'BHARTIARTL.NS',
  'AXISBANK.NS',
  'LT.NS',
  'SBIN.NS',
  'MARUTI.NS',
  'HUL.NS',
  'INDUSINDBK.NS',
  'HDFC.NS',
  'BAJFINANCE.NS',
  'WIPRO.NS',
  'ASIANPAINT.NS',
  'TECHM.NS',
  'NESTLEIND.NS',
  'BAJAJFINSV.NS',
  'BAJAJ-AUTO.NS',
  'TITAN.NS',
  'UPL.NS',
  'SHREECEM.NS',
  'DIVISLAB.NS',
];

export const ApexChart = () => {
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
              {stocks.map((stock, index) => (
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
      <div>
        <h1 style={{fontSize: 50, marginTop: 80, color: '#494949'}}>Relevant News</h1>
        <Box sx={{ width: '80%', padding: '5%', margin: 'auto' }}>
          <Paper
            square
            elevation={0}
            sx={{
              display: 'flex',
              alignItems: 'center',
              height: 80,
              borderTopLeftRadius: 10,
              borderTopRightRadius: 10,
              color: '#fff',
              pl: 2,
              bgcolor: '#0c0c0c',
            }}
          >
            <Typography style={{color: 'dodgerblue', fontSize: 25}}>{images[activeStep]?.title}</Typography>
          </Paper>
          <AutoPlaySwipeableViews
            axis={theme.direction === 'rtl' ? 'x-reverse' : 'x'}
            index={activeStep}
            onChangeIndex={handleStepChange}
            enableMouseEvents
          >
            {images.map((step, index) => (
              <div key={step.title}>
                {Math.abs(activeStep - index) <= 2 ? (
                  <Box
                    component="img"
                    sx={{
                      height: 500,
                      fontSize: 40,
                      display: 'block',
                      overflow: 'hidden',
                      width: '100%',
                    }}
                    src={step.image.toString()}
                    alt={step.URL}
                  />
                ) : null}
              </div>
            ))}
          </AutoPlaySwipeableViews>
          <MobileStepper style={{backgroundColor: '#011222', borderBottomLeftRadius: 10, borderBottomRightRadius: 10}}
            steps={images.length}
            position="static"
            activeStep={activeStep}
            nextButton={
              <Button
                size="small"
                onClick={handleNext}
                disabled={activeStep === images.length - 1}
              >
                Next
                {theme.direction === 'rtl' ? (
                  <KeyboardArrowLeft />
                ) : (
                  <KeyboardArrowRight />
                )}
              </Button>
            }
            backButton={
              <Button size="small" onClick={handleBack} disabled={activeStep === 0}>
                {theme.direction === 'rtl' ? (
                  <KeyboardArrowRight />
                ) : (
                  <KeyboardArrowLeft />
                )}
                Back
              </Button>
            }
          />
        </Box>
      </div>
    </div>
  );
}

export default ApexChart;