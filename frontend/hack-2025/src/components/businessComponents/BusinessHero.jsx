import React from 'react';
import business from '/src/assets/business.webp';
import DropzoneUpload from './DropzoneUpload';

const BusinessHero = () => {
  return (
    <>
    <div
      className="w-full bg-cover bg-center bg-no-repeat relative h-screen"
      style={{ backgroundImage: `url(${business})` }}
    >
      {/* Overlay for darker contrast */}
      <div className="absolute inset-0 bg-black/60"></div>

      {/* Main content */}
      <div className="relative z-10 px-6 py-24 max-w-6xl mx-auto">
        <div className="bg-white/90 backdrop-blur-md rounded-xl shadow-lg p-10 md:p-16 max-w-3xl text-left">
          <p className="uppercase text-[#00A86B] font-bold text-sm tracking-wider mb-2">
            Improve the world
          </p>
          <h1 className="text-3xl md:text-4xl font-extrabold text-[#1A1A1A] mb-4">
            How it works
          </h1>
          <p className="text-gray-700 text-base md:text-lg mb-6 leading-relaxed">
            Upload a <strong>.zip</strong> file containing your Bill of Materials (BOM). We'll process your data and provide insights into your environmental footprint.
          </p>
          
          {/* Upload Zone */}
          <DropzoneUpload />

          {/* Optional CTA */}
          <a href="#formatting">
          <button className="mt-6 bg-[#005F73] text-white font-medium px-6 py-3 rounded-md shadow-md hover:scale-105 transition-all duration-300 ease-in-out">
            Learn More
          </button>
          </a>
        </div>
      </div>
    </div>

    <div id="formatting" className="w-full bg-[#f8f9fa] py-16 px-6">
        <div className="max-w-4xl mx-auto text-center md:text-left">
            <h2 className="text-2xl md:text-3xl font-bold text-[#1A1A1A] mb-6">
                BOM Upload Format Guide
            </h2>
            <p className="text-lg text-gray-700 mb-6">
                To generate accurate sustainability reports, please upload a <strong>.zip</strong> file containing one or more <strong>CSV</strong> files. These files should reflect the structure of your supply chain and match our system requirements.
            </p>

        <h3 className="text-xl font-semibold text-[#00A86B] mb-3">Required Columns</h3>
        <ul className="list-disc list-inside text-gray-700 text-lg space-y-2 mb-6">
            <li><strong>Plant</strong> – Identifier for the plant location.</li>
            <li><strong>PlantSKUQuantity</strong> – Quantity of SKUs produced at the plant.</li>
            <li><strong>Process</strong> – Name of the process used.</li>
            <li><strong>ProcessDefinition</strong> – Description or definition of the process.</li>
            <li><strong>Sku</strong> – Unique identifier for the product SKU.</li>
            <li><strong>SkuBom</strong> – Bill of materials associated with each SKU.</li>
            <li><strong>SkuProcess</strong> – Process steps linked to each SKU.</li>
            <li><strong>Link</strong> – Relationships as defined in the latest ER diagram.</li>
        </ul>

        <p className="text-gray-600 text-base">
            ⚠️ Make sure your .zip file is not password protected, and all files inside are readable CSVs. You can reference our <em>latest ER diagram</em> (coming soon) to understand how your data will be linked in our system.
        </p>
        </div>
    </div>
</>


  );
};

export default BusinessHero;
