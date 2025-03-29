import React, { useEffect, useState } from 'react'
import{FiChevronDown} from 'react-icons/fi'
import ScoreCircle from './ScoreCircle';



const HeroDash = ({ name = 'User ', googleID = '0001'}) => {

const [scores, setScores] = useState({ carbon: 0, water: 0});

useEffect(() => {
    const fetchScores = async () => {
        try{

            const res = await fetch('http://localhost:8000/get_ratings/', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                  googleID: googleID,
                  timeInstance: '2025-03-29_03:17', // Replace later
                }),
              });

        
        const data = await res.json();
        setScores(data);
        } catch(err){
        console.error('Failed to fetch score data:', err);
        }
    };

    fetchScores();

}, [googleID]);

//placeholder for API Data SCORE DATA
const carbon = 451
const water = 300


    return (
        <div className='w-full rounded-sm shadow-md py-16 px-4 '>
            <div className='max-w-[1240px] mx-auto grid md:grid-cols-2 gap-12'>

            {/*Left score chart */}
            <div className="bg-[#1A1A1A] rounded-xl shadow-lg p-8 flex flex-col items-center">
                <h3 className="text-white text-xl font-semibold mb-6">Your Impact</h3>

                <div className="flex flex-col md:flex-row justify-center items-center gap-8 p-4">
                    <div className="flex justify-center">
                        <ScoreCircle label="Carbon" value={scores.carbon} color="#00C49F" />
                    </div>
                    <div className="flex justify-center]">
                        <ScoreCircle label="Water" value={scores.water} color="#0088FE" />
                    </div>
                </div>
            </div>



                {/* Right message */}
                <div className = 'flex flex-col justify-center text-center md:text-left px-6'>
                    <h2 className='text-3xl md:text-4xl font-bold mb-2 text-[#1A1A1A]'>
                        Welcome, {name}
                    </h2>
                    <p className='text-lg text-gray-600 max-w-md'>
                        Scroll to see your full report and breakdown.
                    </p>
                    <div className='mt-6 flex justify-center md:justify-start'>
                        <FiChevronDown size={32} className="text-gray-800 animate-bounce" />
                    </div>
                </div>
            </div>
        </div>
    );
};


export default HeroDash