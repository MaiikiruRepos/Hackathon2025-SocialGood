import React from 'react'

import PlantPieChart from './PlantPieChart'

const HeroReportChart = () => {
    //test data for what API will give back
    const waterUsageByPlant = {
        "00001" : 50,
        "00002" : 50,
    }

    const carbonUsageByPlant = {
        "00001" : 50,
        "00002" : 50,
    }

    
    return (
        <div className= 'w-full py-16 px-4 text-black'>
            <div className = 'max-w-[1240px] mx-auto'>
                <h2 className='text-bold text-center text-black text-2xl py-8'>Reports by plant</h2>
                    <div className = 'flex gap-10 justify-center text-black'>
                        <PlantPieChart title="Water Usage" data={waterUsageByPlant} />
                        <PlantPieChart title="Carbon Usage" data={carbonUsageByPlant} />
                    </div>
            </div>
        </div>
    );
};

export default HeroReportChart; 