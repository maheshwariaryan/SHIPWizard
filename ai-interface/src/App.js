import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './HomePage'; // Import the new HomePage component
import UnderstandingSHIP from './UnderstandingSHIP';
import ClaimGeneration from './ClaimGeneration';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} /> {/* Home Page */}
        <Route path="/understanding-ship" element={<UnderstandingSHIP />} /> {/* Understanding SHIP Page */}
        <Route path="/claim-generation" element={<ClaimGeneration />} /> {/* Understanding SHIP Page */}
      </Routes>
    </Router>
  );
}

export default App;
