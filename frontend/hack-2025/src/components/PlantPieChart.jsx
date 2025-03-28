import React from 'react';
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer
} from 'recharts';

const COLORS = ['#00C49F', '#0088FE', '#FFBB28', '#FF8042', '#AA00FF'];

const PlantPieChart = ({ title, data }) => {
  // Transform the incoming { "00001": 50, "00002": 50 } into [{ name, value }]
  const formattedData = Object.entries(data).map(([plantId, value]) => ({
    name: `Plant ${plantId}`,
    value,
  }));

  return (
    <div className="bg-white rounded-2xl shadow-lg p-6 flex flex-col items-center w-[300px]">
      <h3 className="text-black text-xl font-semibold mb-2">{title}</h3>
      <ResponsiveContainer width={250} height={250}>
        <PieChart>
          <Pie
            data={formattedData}
            dataKey="value"
            nameKey="name"
            cx="50%"
            cy="50%"
            outerRadius={100}
            label
          >
            {formattedData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
};

export default PlantPieChart;
