import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';

const criteriaList = [
  '1. TotalRevenue',
  '2. TotalInvoices',
  '3. ReturnedItems',
  '4. BoughtItems',
  '5. AvgBasketSize',
  '6. AvgSubtotal',
  '7. AvgItemCost',
  '8. RecentPurDate',
];

function SegmentProfile() {
  const { type, count } = useParams();
  const [segmentData, setSegmentData] = useState(null);

  useEffect(() => {
    const fetchSegmentData = async () => {
      try {
        const response = await fetch(`http://localhost:5000/api/segmentprofile/${type}/${count}`);
        const data = await response.json();
        setSegmentData(data);
      } catch (error) {
        console.error('Error fetching segment data:', error);
      }
    };

    fetchSegmentData();
  }, [type, count]);

  if (!segmentData) {
    return <div>Loading...</div>;
  }

  const renderSegmentStats = () => {
    const stats = segmentData.segment_stats[0];
    return Object.entries(stats).map(([key, value]) => (
      <li className="customer-metric" key={key}>
        <strong>{key}:</strong> {value}
      </li>
    ));
  };

  return (
    <div className='pp'>
      <div className='cc'>
      <h2 className="customer-metrics-heading">{segmentData.criteria_vector[0]['Segment Name']}</h2>
      <h2 className="customer-metrics-heading">Customers</h2>
      </div>

      <div className='cc'>
      <h2 className="customer-metrics-heading">Depends On:</h2>
      <pre className="customer-metric-item">{segmentData.criteria_vector[0]['Criteria Array']}</pre>
      <ul className="customer-metric-item">
        {criteriaList.map((criteria, index) => (
          <li  className="customer-metric" key={index}>{criteria}</li>
        ))}
      </ul>
      </div>

      <div className='cc'>
      <h2 className="customer-metrics-heading">Top {count} Customers:</h2>
      <h3>   ID  | {type} Score</h3>
      <ul>
        {segmentData.customerlist.map((customer) => (
          <li  className="customer-metric-item" key={customer.CustomerID}>
            <Link to={`/customer/${customer.CustomerID}`}>
              {customer.CustomerID} | {customer[type + 'Score']}
            </Link>
          </li>
        ))}
      </ul>
      </div>

      <div className='cc'>
      <h2 className="customer-metrics-heading">{type} Stats (Top {count}):</h2>
      <ul  className="customer-metric-item">{renderSegmentStats()}</ul>
      </div>
    </div>
  );
}

export default SegmentProfile;
