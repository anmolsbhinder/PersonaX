import React from 'react';
import Navbar from './home/Navbar';
import Homepage from './pages/Homepage';
import { BrowserRouter as Router, Route, Routes} from 'react-router-dom'
import './App.css';
import CustomerProfile from './pages/CustomerProfile';
import Segmentpage from './pages/Segmentpage';
import SegmentProfile from './pages/SegmentProfile';
import CustomSegment from './pages/CustomSegment';

function App() {
  return (
    <Router>
      <Navbar/>
      <Routes>
        <Route exact path='/' element={<Homepage/>}/>
        <Route exact path='/customer/:customer_id' element={<CustomerProfile/>}/>
        <Route exact path='/segment' element={<Segmentpage/>}/>
        <Route path='/segment/:type/:count' element={<SegmentProfile/>}/>
        <Route path='/segment/:type/:count/:values' element={<CustomSegment/>}/>
      </Routes>
    </Router>
    

  );
}

export default App;
