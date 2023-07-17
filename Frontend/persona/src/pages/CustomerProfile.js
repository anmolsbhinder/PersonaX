import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import MyBarChart from '../components/MyBarChart';


function CustomerProfile() {
  const { customer_id } = useParams();
  const [customerDetails, setCustomerDetails] = useState(null);

  useEffect(() => {
    const fetchCustomerDetails = async () => {
      try {
        // Fetch customer details from the Flask API
        const response = await fetch(`http://localhost:5000/api/customerprofile/${customer_id}`);
        const data = await response.json();

        setCustomerDetails(data);
      } catch (error) {
        console.error('Error fetching customer details:', error);
      }
    };

    fetchCustomerDetails();
  }, [customer_id]);

  if (!customerDetails) {
    return <div>Loading...</div>;
  }

  const sortArrayByScoreDescending = (array) => {
    return array.sort((a, b) => {
      const aScores = Object.values(a).filter(value => typeof value === 'number');
      const bScores = Object.values(b).filter(value => typeof value === 'number');
      return Math.max(...bScores) - Math.max(...aScores);
    });
  };

  const convertedSegmentScores = customerDetails.segment_scores[0]
    ? Object.keys(customerDetails.segment_scores[0]).map(key => ({
        name: key,
        score: customerDetails.segment_scores[0][key]
      }))
    : [];

  const convertedCriteriaScores = customerDetails.criteria_scores[0]
    ? Object.keys(customerDetails.criteria_scores[0]).map(key => ({
        name: key,
        score: customerDetails.criteria_scores[0][key]
      }))
    : [];

  return (
  <div className='pp'>

    <div className='cc'>
      <h2 className="customer-metrics-heading">Customer Metrics:</h2>
      {sortArrayByScoreDescending(customerDetails.criteria).map((item, index) => (
        <div key={index} className="customer-metric-item">
          {Object.entries(item).map(([key, value]) => (
            <p className="customer-metric" key={key}>
              <strong>{key}:</strong> {value}
            </p>
          ))}
        </div>
      ))}
      </div>

    <div className='cc'>
      <h2 className="customer-metrics-heading">Customer Metric Scores:</h2>
      {sortArrayByScoreDescending(customerDetails.criteria_scores).map((item, index) => (
        <div className="customer-metric-item" key={index}>
          {Object.entries(item).map(([key, value]) => (
            <p className="customer-metric" key={key}>
              <strong>{key}:</strong> {value}
            </p>
          ))}
        </div>
      ))}

      <div className='bar'>
        {convertedSegmentScores.length > 0 && <MyBarChart data={convertedCriteriaScores} />}
      </div>

    </div>    
    
    <div className='cc'>
      <h2 className="customer-metrics-heading">Category Scores:</h2>
      {sortArrayByScoreDescending(customerDetails.segment_scores).map((item, index) => (
        <div className="customer-metric-item" key={index}>
          {Object.entries(item).map(([key, value]) => (
            <p className="customer-metric" key={key}>
              <strong>{key}:</strong> {value}
            </p>
          ))}
        </div>
      ))}

      <div className='bar'>
        {convertedSegmentScores.length > 0 && <MyBarChart data={convertedSegmentScores} />}
      </div>
    </div>

      </div>
  );
};

export default CustomerProfile;
