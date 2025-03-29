import React from 'react'
import {
    RadialBarChart,
    RadialBar,
    Legend,
    ResponsiveContainer,
    Tooltip
} from 'recharts'
import{FiChevronDown} from 'react-icons/fi'
import ScoreCircle from './ScoreCircle';



const HeroDash = ({ name = 'User '}) => {
//placeholder for API Data
const carbon = 451
const water = 300


    return (
        <div className='w-full bg-black py-16 px-4'>
            <div className='max-w-[1240px] mx-auto grid md:grid-cols-2'>

            {/*Left score chart */}
            <div className=' w-full h-[300px] flex justify-center'>
            <ScoreCircle label="Carbon" value={carbon} color="#00C49F" />
            <ScoreCircle label="Water" value={water} color="#0088FE" />
            </div>



                {/* Right message */}
                <div className = 'flex flex-col justify-center text-center md:text-left px-6'>
                    <h2 className='text-3xl md:text-4xl font-bold mb-2 text-white'>
                        Welcome, {name}
                    </h2>
                    <p className='text-lg text-gray-300'>
                        Scroll to see your full report and breakdown.
                    </p>
                    <div className='mt-6 flex justify-center md:justify-start'>
                        <FiChevronDown size={32} className="text-amber-500 animate-bbounce" />
                    </div>
                </div>
            </div>
        </div>
    );
};


export default HeroDash