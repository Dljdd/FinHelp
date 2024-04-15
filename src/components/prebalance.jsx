import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack'
import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import { PieChart } from '@mui/x-charts/PieChart';
import Navbar from "./Navbar.jsx";
import { NavLink } from 'react-router-dom'; // Import NavLink from react-router-dom
import { useState } from 'react';

function Rebalance() {
  const [nav, setNav] = useState(false); // Move useState inside the component function

  const calculateWeight = (assetValue, totalPortfolioValue) => {
    return (assetValue / totalPortfolioValue) * 100;
  };

  function createData(name, original, currentvalue, totalPortfolioValue) {
    const originalValue = parseFloat(original.replace('$', ''));
    const currentValue = parseFloat(currentvalue.replace('$', ''));
    const currentReturnPercent = ((currentValue - originalValue) / originalValue) * 100;
    const profitloss = currentValue - originalValue;
    const weight = calculateWeight(currentValue, totalPortfolioValue);
    return { name, original, currentReturnPercent, currentvalue, profitloss, weight };
  }

  const rowsData = [
    { name: 'Asset 1', original: '$1000', currentvalue: '$1100' },
    { name: 'Asset 2', original: '$1500', currentvalue: '$1575' },
    { name: 'Asset 3', original: '$800', currentvalue: '$920' },
    { name: 'Asset 4', original: '$2000', currentvalue: '$2160' },
    { name: 'Asset 5', original: '$1200', currentvalue: '$1344' },
  ];

  const totalPortfolioValue = rowsData.reduce((total, row) => total + parseFloat(row.currentvalue.replace('$', '')), 0);

  const rows = rowsData.map(row => createData(row.name, row.original, row.currentvalue, totalPortfolioValue));

  const pieChartData = rows.map((row, index) => ({
    id: index,
    value: row.weight,
    label: row.name,
  }));

  return (
    <div>
      <Navbar />
      <div style={{display: 'flex', marginTop: 50, marginLeft: 40, marginRight: 80, justifyContent: 'space-between',alignItems: 'center', minHeight: 350, minWidth: 180}}>
        <PieChart 
          series={[{ data: pieChartData }]}
          width={1000}
          height={800}
        />
        <TableContainer style={{}} component={Paper}>
          <Table sx={{  minHeight: 500, minWidth: 400 }} aria-label="simple table">
            <TableHead>
              <TableRow>
                <TableCell>Asset </TableCell>
                <TableCell align="right">Orignal Investment</TableCell>
                <TableCell align="right">Return&nbsp;%</TableCell>
                <TableCell align="right">Current Value</TableCell>
                <TableCell align="right">Profit/Loss</TableCell>
                <TableCell align="right">Weight of Asset</TableCell>
              </TableRow>
            </TableHead>
            <TableBody style={{ minHeight: 700, minWidth: 300 }}>
              {rows.map((row) => (
                <TableRow
                  key={row.name}
                  sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                >
                  <TableCell component="th" scope="row">{row.name}</TableCell>
                  <TableCell align="right">{row.original}</TableCell>
                  <TableCell align="right">{row.currentReturnPercent.toFixed(2)}%</TableCell>
                  <TableCell align="right">{row.currentvalue}</TableCell>
                  <TableCell align="right">{row.profitloss}</TableCell>
                  <TableCell align="right">{row.weight.toFixed(3)}%</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
        <div style={{ marginLeft: 'auto', justifyContent: 'flex-end', marginTop: 700, marginRight: 50}}>
          <NavLink to='/home' activeClassName='active' smooth={true} duration={500}>
            <Button variant="outlined" size='large'>Rebalance Me</Button>
          </NavLink>
        </div>
      </div>
    </div>
  );
}

export default Rebalance;
