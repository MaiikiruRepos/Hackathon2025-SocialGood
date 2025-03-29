import React from 'react';
import aboutImage from '/src/assets/aboutImage.webp';

const About = () => {
  return (
    <div className="w-full bg-white py-16 px-4">
      <div className=" mx-auto flex flex-col md:flex-row overflow-hidden rounded-2xl shadow-lg">
        
        {/* Left Side Image */}
        <div
          className="w-full md:w-1/2 h-64 md:h-auto bg-cover bg-center"
          style={{ backgroundImage: `url(${aboutImage})` }}
        />

        {/* Right Side Content */}
        <div className="w-full md:w-1/2 bg-[#1A1A1A] text-white p-8 md:p-12 flex flex-col justify-center">
          
          {/* About Us Section */}
          <div className="mb-10">
            <h2 className="text-3xl font-bold mb-4">About Us</h2>
            <ul className="text-lg text-gray-400 list-disc pl-5 space-y-2">
              <li>Empowering sustainability through data</li>
              <li>Helping businesses reduce environmental impact</li>
              <li>Simplifying carbon and water tracking</li>
              <li>Transforming supply chains for a greener future</li>
            </ul>
          </div>

          {/* What We Do Section */}
          <div>
            <h2 className="text-3xl font-bold mb-4">What We Do</h2>
            <ul className="text-lg text-gray-400 list-disc pl-5 space-y-2">
              <li>Upload standard BOM</li>
              <li>Calculate carbon emissions</li>
              <li>Track water usage</li>
              <li>Generate sustainability score</li>
              <li>Provide actionable insights</li>
            </ul>
          </div>

        </div>
      </div>
    </div>
  );
};

export default About;

