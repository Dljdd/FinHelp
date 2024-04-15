import * as React from 'react';
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
import Navbar from "./Navbar.jsx";

const AutoPlaySwipeableViews = autoPlay(SwipeableViews);
const images = [
  {
    label: 'Navigating the Markets: A Comprehensive Guide to Trading',
    imgPath:
      'https://miro.medium.com/v2/resize:fit:1144/format:webp/1*Eeyu27Ulkg3ywJx8N_UcTA.jpeg',
    content: 'San Francisco – Oakland Bay Bridge, United States',
    url: 'https://medium.com/@kapilcool/navigating-the-markets-a-comprehensive-guide-to-trading-9e142990de4c'
  },
  {
    label: 'Mastering the Bull Call Spread Strategy: A Deeper Dive',
    imgPath:
      'https://miro.medium.com/v2/resize:fit:1400/format:webp/0*5zzY0cAF43LMwrBl',
      content: 'San Franciand Bay Bridge, United States',
      url: 'https://medium.com/@laabhumsocial/mastering-the-bull-call-spread-strategy-a-deeper-dive-cd15efc60b20'
  },
  {
    label: 'The Martingale Strategy: Is It Really 100% Profitable?',
    imgPath:
      'https://miro.medium.com/v2/resize:fit:1400/format:webp/1*cv2GEpxraujdgCf0icbSBA.png',
      content: 'San FranOakland Bay Bridge, United States',
      url: 'https://medium.com/@keenpeachy119/the-martingale-strategy-is-it-really-100-profitable-ed64c4055a9a'
  }
];

function Community() {
  const theme = useTheme();
  const [activeStep, setActiveStep] = React.useState(0);
  const maxSteps = images.length;

  const handleNext = () => {
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };

  const handleStepChange = (step) => {
    setActiveStep(step);
  };

  return (
    <div>
      <div style={{marginBottom: 20}}>
      <Navbar />
      </div>
    <h1 style={{fontSize: 100, marginTop: 90, fontWeight: 'bold', color: '#494949'}}>The power of community</h1>
    <h1 style={{fontSize: 50, marginTop: 80, color: '#494949'}}>Educational Content</h1>
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
        <Typography style={{color: 'dodgerblue', fontSize: 25}}>{images[activeStep].label}</Typography>
      </Paper>
      <AutoPlaySwipeableViews
        axis={theme.direction === 'rtl' ? 'x-reverse' : 'x'}
        index={activeStep}
        onChangeIndex={handleStepChange}
        enableMouseEvents
      >
        {images.map((step, index) => (
          <div key={step.label}>
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
                src={step.imgPath}
                alt={step.label}
              />
            ) : null}
          </div>
        ))}
      </AutoPlaySwipeableViews>
      <MobileStepper style={{backgroundColor: '#011222', borderBottomLeftRadius: 10, borderBottomRightRadius: 10}}
        steps={maxSteps}
        position="static"
        activeStep={activeStep}
        nextButton={
          <Button
            size="small"
            onClick={handleNext}
            disabled={activeStep === maxSteps - 1}
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
    <h1 style={{fontSize: 50, marginTop: 20, color: '#494949'}}>Trading Ideas</h1>
    <Box sx={{ width: '80%', padding: '5%', margin: 'auto' }}>
    <Paper
        square
        elevation={0}
        sx={{
          display: 'flex',
          alignItems: 'center',
          color: '#fff',
          height: 80,
          borderTopLeftRadius: 10,
          borderTopRightRadius: 10,
          pl: 2,
          bgcolor: '#0c0c0c',
        }}
      >
        <Typography style={{color: 'dodgerblue', fontSize: 25}}>{images[activeStep].content}</Typography>
      </Paper>
      <AutoPlaySwipeableViews
        axis={theme.direction === 'rtl' ? 'x-reverse' : 'x'}
        index={activeStep}
        onChangeIndex={handleStepChange}
        enableMouseEvents
      >
        {images.map((step, index) => (
          <div key={step.content}>
            {Math.abs(activeStep - index) <= 2 ? (
              <Box
                component="img"
                sx={{
                  height: 500,
                  display: 'block',
                  overflow: 'hidden',
                  width: '100%',
                }}
                src={step.imgPath}
                alt={step.content}
              />
            ) : null}
          </div>
        ))}
      </AutoPlaySwipeableViews>
      <MobileStepper style={{backgroundColor: '#011222', borderBottomLeftRadius: 10, borderBottomRightRadius: 10}}
        steps={maxSteps}
        position="static"
        activeStep={activeStep}
        nextButton={
          <Button
            size="small"
            onClick={handleNext}
            disabled={activeStep === maxSteps - 1}
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
  );
}

export default Community;


