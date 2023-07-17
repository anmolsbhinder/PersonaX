import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import photo from '../Resources/Red.png';
import Input from '@mui/joy/Input';
import Button from '@mui/joy/Button';



function Homepage() {
  const [customerId, setCustomerId] = useState('');
  const navigate = useNavigate();

  const handleCustomerIdChange = (event) => {
    setCustomerId(event.target.value);
  };

  const handleViewDetails = () => {
    // Navigate to the customer details page with the provided customer ID
    navigate(`/customer/${customerId}`);
  };

  const handleGoToSegmentPage = () => {
    console.log("in home")
    // Navigate to the segment page
    navigate('/segment');
  };

  return (
    <div>
      <img src={photo} className='px' alt=''/>
    <div className='homeinputs'>   
      {/* <img src={photo2} className='px2'/> */}
      <div className='inp_button'>
      <Input className='cidinput' color="danger" size="lg"
        type="text"
        value={customerId}
        onChange={handleCustomerIdChange}
        placeholder="Enter Customer ID"
        sx={{ '--Input-focused': 1, width: 256 }}
      />
      <Button color="danger" size="lg" onClick={handleViewDetails}>View Customer Profile</Button>
      </div>
      <div className='segpg'>
        <Button color="danger" size="lg" onClick={handleGoToSegmentPage}>Customer Categories</Button>
      </div>
    </div>
    </div>
  );
}

export default Homepage;
