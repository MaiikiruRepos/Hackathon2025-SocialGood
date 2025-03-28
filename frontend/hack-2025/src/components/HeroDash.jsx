import React from 'react'
import {
    PieChart,
    Pie,
    Cell,
    ResponsiveContainer,
    Tooltip
} from 'recharts'
import{FiChevronDown} from 'react-icons/fi'


//placeholder for API Data
const data = [
    { name: 'Used', value: 75},
    { name: 'Remaining', value: 25}
];

const COLORS = ['#00C49F', '#FFBB28']

const HeroDash = ({ name = 'User '}) => {
    return (
        <div className='w-full bg-black py-16 px-4'>
            <div className='max-w-[1240px] mx-auto grid md:grid-cols-2'>

            {/*Left score chart */}
            <div className='flex justify-center'>
                <ResponsiveContainer width={250} height={250}>
                    <PieChart>
                        <Pie
                        data = {data}
                        dataKey="value"
                        nameKey="name"
                        cx="50%"
                        cy="50%"
                        outerRadius={100}
                        fill="#8884d8"
                        label
                    >
                    {data.map((entry, index) => (
                        <Cell key={'cell-${index}'} fill={COLORS[index % COLORS.length]} />
                    ))}
                        </Pie>
                        <Tooltip />
                    </PieChart>
                </ResponsiveContainer>
            </div>



                {/* Right message */}

                <div>

                </div>

            </div>
        </div>
    );
};


export default HeroDash