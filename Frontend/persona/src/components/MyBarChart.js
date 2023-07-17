import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

const MyBarChart = ({ data }) => {
  return (
    <BarChart width={400} height={300} data={data}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="name" />
      <YAxis />
      <Tooltip />
      <Legend />
      <Bar dataKey="score" fill="#8884d8" />
      {/* <Bar dataKey="score" fill="#D3232F" /> */}
    </BarChart>
  );
};

export default MyBarChart;
