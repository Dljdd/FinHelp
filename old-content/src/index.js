import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import { Auth0Provider } from '@auth0/auth0-react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'; // Import BrowserRouter, Routes, and Route
import Home from './components/Home';
import ApexChart from './components/Chart';
import Community from './components/Community';
import BasicTable from './components/Table';
import Crypto from './components/Crypto';
import About from './components/About';
import Work from './components/Work';
import Rebalance from './components/prebalance';
ReactDOM.render(
  <React.StrictMode>
    <Auth0Provider
      domain="dev-vgdwcqt11qrihuga.us.auth0.com"
      clientId="SlFcLOHmgm7EBJjUdYUKAhwxFQ4cVtxQ"
      authorizationParams={{
        redirect_uri: window.location.origin
      }}
    >
      <Router>
        <Routes>
          <Route path='/' element={<App />} />
          <Route path='/stock' element={<ApexChart />} />
          <Route path='/portfolio' element={<BasicTable />} />
          <Route path='/community' element={<Community />} />
          <Route path='/crypto' element={<Crypto />} />
          <Route path='/About' element={<About />} />
          <Route path='/home' element={<Home />} />
          <Route path='*' element={<Home />} />
          <Route path='/work' element={<Work />} />
          <Route path='/rebalance' element={<Rebalance />} />
        </Routes>
      </Router>
    </Auth0Provider>
  </React.StrictMode>,
  document.getElementById('root')
);
