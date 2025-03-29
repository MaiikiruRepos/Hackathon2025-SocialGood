import React from 'react';
import business from '/src/assets/business.jpg';
import DropzoneUpload from './DropzoneUpload';

const BusinessHero = () => {
  return (
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
          <button className="mt-6 bg-[#005F73] text-white font-medium px-6 py-3 rounded-md shadow-md hover:scale-105 transition-all duration-300 ease-in-out">
            Learn More
          </button>
        </div>
      </div>
    </div>
  );
};

export default BusinessHero;
