import React, { useState, useEffect } from 'react';
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
  const [googleID, setGoogleID] = useState('000001'); // Default to "1"
  const [updatedData, setUpdatedData] = useState(mockData);

  const updateDataForGoogleID = (id) => {
    if (id) {
      const updatedMockData = JSON.parse(JSON.stringify(mockData)); // deep copy
      updatedMockData.plant["00001"].sku["001"].Description = `Updated Apple for ${id}`;
      updatedMockData.plant["00002"].sku["001"].Description = `Updated Banana for ${id}`;
      setUpdatedData(updatedMockData);
    }
  };

  useEffect(() => {
    updateDataForGoogleID(googleID);
  }, [googleID]);

  const handleGoogleIDChange = (e) => {
    setGoogleID(e.target.value);
  };

  return (
    <div>
      <Navbar />

        {/* GoogleID Dropdown */}
        <div className="bg-white p-4">
          <div className="flex justify-end space-x-2">
            <select
              value={googleID}
              onChange={handleGoogleIDChange}
              className="p-2 border rounded"
            >
              <option value="000001">000001</option>
              <option value="ai_user">AI Company</option>
              <option value="lego_user">Lego</option>
              <option value="insurance_user">Insurance Company</option>
            </select>
          </div>
        </div>

      <HeroDash googleID={googleID} />

      <div className='bg-white min-h-screen'>
        <SkuTable googleID={googleID} />
      </div>
    </div>
  );
};

export default Dashboard;
