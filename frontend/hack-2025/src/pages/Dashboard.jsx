import React, { useState } from 'react';
import HeroDash from '../components/HeroDash';
import Navbar from '../components/Navbar';
import HeroReportChart from '../components/HeroReportCharts';
import SkuTable from '../components/SkuTable';

const mockData = {
  plant: {
    "00001": {
      sku: {
        "001": {
          Description: "example apple",
          CarbonLB: "56",
          WaterGal: "65",
        },
        "002": {
          Description: "example pear",
          CarbonLB: "45",
          WaterGal: "32",
        },
      },
    },
    "00002": {
      sku: {
        "001": {
          Description: "example banana",
          CarbonLB: "70",
          WaterGal: "80",
        },
      },
    },
  },
};

const Dashboard = () => {
  const [googleID, setGoogleID] = useState('');
  const [updatedData, setUpdatedData] = useState(mockData);  // State to store updated data

  const handleGoogleIDChange = (e) => {
    const newGoogleID = e.target.value;
    setGoogleID(newGoogleID);

    // Update the data based on googleID
    if (newGoogleID) {
      const updatedMockData = { ...mockData };
      updatedMockData.plant["00001"].sku["001"].Description = `Updated Apple for ${newGoogleID}`;
      updatedMockData.plant["00002"].sku["001"].Description = `Updated Banana for ${newGoogleID}`;

      setUpdatedData(updatedMockData);  // Update state with new data
    }
  };

  return (
    <div>
      <Navbar />

      {/* Input for GoogleID */}
      <div className="bg-white p-4">
        <div className="flex justify-end space-x-2">
          <input
            type="text"
            placeholder="Enter GoogleID"
            value={googleID}
            onChange={handleGoogleIDChange}
            className="p-2 border rounded"
          />
        </div>
      </div>

      <HeroDash googleID={googleID} />

      <div className='bg-white min-h-screen'>
        <SkuTable rawData={updatedData} />
      </div>
    </div>
  );
};

export default Dashboard;
