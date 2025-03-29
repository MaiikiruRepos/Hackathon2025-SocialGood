import React from 'react';
import {
  RadialBarChart,
  RadialBar,
  ResponsiveContainer
} from 'recharts';

const ScoreCircle = ({ label, value, max = 1000, color = '#00C49F' }) => {
  const percentage = (value / max) * 100;

  const data = [
    { name: 'progress', value: percentage, fill: color },
    { name: 'max', value: 100, fill: '#FFFFFF' }, // background ring
  ];

  return (
    <div className="relative w-[200px] h-[200px] md:w-[250px] md:h-[250px]">
      <ResponsiveContainer width="100%" height="100%">
        <RadialBarChart
          innerRadius="70%"
          outerRadius="100%"
          data={data}
          startAngle={90}
          endAngle={-270}
        >
          <RadialBar
            dataKey="value"
            background
            cornerRadius={50}
          />
        </RadialBarChart>
      </ResponsiveContainer>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <p className="text-white text-xl font-semibold">{label}</p>
        <p className="text-white text-xl font-bold">
          {value}
        </p>
      </div>
    </div>
  );
};

export default ScoreCircle;
