import React, {useEffect, useState } from 'react'
import PlantPieChart from './PlantPieChart'

const HeroReportChart = ({googleID = '000001', timeInstance = ''}) => {
    /*test data for what API will give back
    const waterUsageByPlant = {
        "00001" : 50,
        "00002" : 50,
    }

    const carbonUsageByPlant = {
        "00001" : 50,
        "00002" : 50,
    }
*/

    const [waterUsageByPlant, setWaterUsageByPlant] = useState({});
    const [carbonUsageByPlant, setCarbonUsageByPlant] = useState({});

    useEffect(() => {
        if (!timeInstance) return;

        const fetchPlantData = async () => {
            try{
                const [carbonRes, waterRes] = await Promise.all([
                    fetch('http://localhost:8000/get_plant_carbon/',{
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ googleID, timeInstance }),
                    }),
                    fetch('http://localhost:8000/get_plant_water/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ googleID, timeInstance}),
                    }),
                ]);

                const carbonData = await carbonRes.json();
                const waterData = await waterRes.json();

                setCarbonUsageByPlant(carbonData.plant || {});
                setWaterUsageByPlant(waterData.plant || {});
            } catch (err) {
                console.error('Error fetching plant data:', err);
            }
        };

        fetchPlantData();
    }, [googleID, timeInstance]);




    
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