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
  // Transform { "00001": 50, "00002": 50 } into [{ name, value }]
  const formattedData = Object.entries(data).map(([plantId, value]) => ({
    name: `Plant ${plantId}`,
    value,
  }));

  // Custom label renderer (places % labels outside the pie)
  const RADIAN = Math.PI / 180;
  const renderCustomizedLabel = ({ cx, cy, midAngle, outerRadius, percent }) => {
    const radius = outerRadius + 20;
    const x = cx + radius * Math.cos(-midAngle * RADIAN);
    const y = cy + radius * Math.sin(-midAngle * RADIAN);

    return (
      <text
        x={x}
        y={y}
        fill="#000"
        textAnchor={x > cx ? 'start' : 'end'}
        dominantBaseline="central"
        fontSize={14}
      >
        {`${(percent * 100).toFixed(0)}%`}
      </text>
    );
  };

  return (
    <div className="rounded-lg shadow-xl p-6 my-4 flex flex-col items-center w-[500px] hover:scale-105 duration-300">
      <h3 className="text-black text-2xl font-semibold mb-8">{title}</h3>
      <ResponsiveContainer width={350} height={350}>
        <PieChart>
          <Pie
            data={formattedData}
            dataKey="value"
            nameKey="name"
            cx="50%"
            cy="50%"
            outerRadius={100}
            label={renderCustomizedLabel}
          >
            {formattedData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip formatter={(value) => `${value} units`} />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
};

export default PlantPieChart;
