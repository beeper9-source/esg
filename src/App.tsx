import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { Box } from '@mui/material';
import Navigation from './components/Navigation';
import Dashboard from './pages/Dashboard';
import Scope1 from './pages/Scope1';
import Scope2 from './pages/Scope2';
import Scope3 from './pages/Scope3';
import CircularEconomy from './pages/CircularEconomy';
import Ideas from './pages/Ideas';

function App() {
  return (
    <Box sx={{ display: 'flex', minHeight: '100vh' }}>
      <Navigation />
      <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/scope1" element={<Scope1 />} />
          <Route path="/scope2" element={<Scope2 />} />
          <Route path="/scope3" element={<Scope3 />} />
          <Route path="/circular-economy" element={<CircularEconomy />} />
          <Route path="/ideas" element={<Ideas />} />
        </Routes>
      </Box>
    </Box>
  );
}

export default App;

