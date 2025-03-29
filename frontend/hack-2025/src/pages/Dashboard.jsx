import React from 'react'
import HeroDash from '../components/HeroDash';
import Navbar from '../components/Navbar'
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
    return (
<div>
    <Navbar />
    <HeroDash />
    <div className = 'bg-white min-h screen'>
        <SkuTable rawData={mockData} />
    </div>
</div>
    );
};
  
  export default Dashboard;
  