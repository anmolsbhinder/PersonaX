import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import CriteriaSelection from '../components/CriteriaSelection';
import Input from '@mui/joy/Input';
import Button from '@mui/joy/Button';
import List from '@mui/joy/List';
import ListItem from '@mui/joy/ListItem';
import Radio from '@mui/joy/Radio';
import RadioGroup from '@mui/joy/RadioGroup';

function Segmentpage() {

    const [segmentlist, setSegmentList] = useState(null);
    const [selectedSegment, setSelectedSegment] = useState('');
    const [count, setCount] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        
        const fetchSegmentList = async () => {
          try {
            
            // Fetch customer details from the Flask API
            const response = await fetch(`http://localhost:5000/api/segmentpg`);
            const data = await response.json();
    
            setSegmentList(data);
          } catch (error) {
            console.error('Error fetching customer details:', error);
          }
        };
        
        fetchSegmentList();
      },[]);

      const handleSegmentSelect = (event) => {
        setSelectedSegment(event.target.value);
      };

      const handleCountChange = (event) => {
        const count = event.target.value;
        setCount(count);
      };

      const handleSubmit = (event) => {
        event.preventDefault();
        
        // Navigate to segment profile page with the selected segment
        navigate(`/segment/${selectedSegment}/${count}`);
      };
    
      if (!segmentlist) {
        return <div>Loading...</div>;
      }

  return (
    <div className='parent'>
        <div className='child1'>
        <h1>Categories</h1>
      <form onSubmit={handleSubmit} className='inp_button'>

<RadioGroup aria-label="Your plan" name="people" >
      <List
        sx={{
          minWidth: 240,
          '--List-gap': '0.5rem',
          '--ListItem-paddingY': '1rem',
          '--ListItem-radius': '8px',
          '--ListItemDecorator-size': '32px',
        }}
      >
        {segmentlist.map((item, index) => (
          <ListItem
            variant="outlined"
            key={item}
            // color="danger"
            sx={{ boxShadow: 'sm', bgcolor: 'background.body'}}
          >

            <Radio
              overlay
              value={item}
              // color="danger"
              onChange={handleSegmentSelect}
              label={item}
              sx={{ flexGrow: 1, flexDirection: 'row-reverse' }}
              slotProps={{
                action: ({ checked }) => ({
                  sx: (theme) => ({
                    ...(checked && {
                      inset: -1,
                      border: '2px solid',
                      borderColor: theme.vars.palette.primary[500],
                    }),
                  }),
                }),
              }}
            />
          </ListItem>
        ))}
      </List>
    </RadioGroup>



         <label>
          <Input className='cidinput' size="lg"
            type="number"
            value={count}
            placeholder="No: of Customers"
            onChange={handleCountChange}
          />
        </label>

        <Button color="danger" size="lg" type="submit">Submit</Button>
      </form>
        </div>

        <div className='child2'>
            <CriteriaSelection></CriteriaSelection>
        </div>
      
    </div>
  )
}

export default Segmentpage