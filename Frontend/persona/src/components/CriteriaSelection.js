import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Box from '@mui/joy/Box';
import Checkbox, { checkboxClasses } from '@mui/joy/Checkbox';
import Sheet from '@mui/joy/Sheet';
import Input from '@mui/joy/Input';
import Button from '@mui/joy/Button';


function CriteriaSelection() {
  const criteriaList = [
    'TotalRevenue',
    'TotalInvoices',
    'ReturnedItems',
    'BoughtItems',
    'AvgBasketSize',
    'AvgSubtotal',
    'AvgItemCost',
    'RecentPurDate',
  ];

  const [selectedCriteria, setSelectedCriteria] = useState([]);
  const [stringValue, setStringValue] = useState('');
  const [countValue, setCountValue] = useState();
  const navigate = useNavigate();

  const handleCheckboxChange = (e) => {
    const { value, checked } = e.target;

    if (checked) {
      setSelectedCriteria((prevSelected) => [...prevSelected, value]);
    } else {
      setSelectedCriteria((prevSelected) =>
        prevSelected.filter((criteria) => criteria !== value)
      );
    }
  };

  const handleStringChange = (e) => {
    setStringValue(e.target.value);
  };

  const handleCountChange = (e) => {
    setCountValue(Number(e.target.value));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Do something with the selected criteria, string value, and count value
    // console.log(selectedCriteria);
    // console.log(stringValue);
    // console.log(countValue);

    navigate(`/segment/${stringValue}/${countValue}/${selectedCriteria}`);
  };

  return (
    <div>
      <h1>Create Category</h1>
      <form onSubmit={handleSubmit} className='inp_button'>
      <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        gap: 2,
        width: 300,
        // boxShadow: 'sm',
        '& > div': { p: 2, boxShadow: 'sm', borderRadius: 'xs', display: 'flex' },
      }}
    >
      {criteriaList.map((criteria, index) => (
          <div key={index}>
            
            <Sheet variant="outlined" sx={{ bgcolor: 'background.body' }}>
                <Checkbox overlay label="High" 
                value={index + 1}
                checked={selectedCriteria.includes(`${index + 1}`)}
                onChange={handleCheckboxChange}/>
            </Sheet>
            <Sheet variant="outlined" sx={{ bgcolor: 'background.body' }}>
                <Checkbox overlay label="Low" 
                value={-(index + 1)}
                checked={selectedCriteria.includes(`-${index + 1}`)}
                onChange={handleCheckboxChange}/>
            </Sheet>
            &nbsp;&nbsp;{criteria}
          </div>
          
        ))}
        </Box>
        
        <div>
          <label>
            <Input className='cidinput'  type="text" value={stringValue} onChange={handleStringChange}
            placeholder="Category Name" />
          </label>
        </div>
        <div>
          <label>
            <Input className='cidinput' type="number" value={countValue} onChange={handleCountChange} 
            placeholder="No: of Customers"/>
          </label>
        </div>
        <Button color="danger" size="lg" type="submit">Submit</Button>
      </form>
    </div>
  );
}

export default CriteriaSelection;
