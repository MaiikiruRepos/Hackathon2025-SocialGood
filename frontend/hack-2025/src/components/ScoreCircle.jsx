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
    { name: 'max', value: 100, fill: '#2d2d2d' }, // background ring
  ];

  return (
    <div className="flex flex-col items-center w-[150px]">
      <ResponsiveContainer width={150} height={150}>
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
      <div className="text-center mt-2">
        <p className="text-white text-sm font-medium">{label}</p>
        <p className="text-amber-400 text-lg font-bold">
          {value} / {max}
        </p>
      </div>
    </div>
  );
};

export default ScoreCircle;
