import React from 'react';
import aboutImage from '/src/assets/forest_bg.png'; // Replace with your image path

const About = () => {
  return (
    <div className="w-full flex flex-col md:flex-row bg-gray-100 py-10">
      {/* Left side with image */}
      <div className="w-full md:w-1/2 bg-cover bg-center"
           style={{ backgroundImage: `url(${aboutImage})`, height: "50vh" }}>
        {/* Image will fill the left half and have a max height of 50vh */}
      </div>

      {/* Right side with two blocks */}
      <div className="w-full md:w-1/2 flex flex-col justify-center px-6 md:px-12 py-6">
        {/* About Us Block */}
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-gray-800">About Us</h2>
          <ul className="text-lg text-gray-600 mt-4 list-disc pl-6 space-y-2">
            <li>Empowering sustainability through data</li>
            <li>Helping businesses reduce environmental impact</li>
            <li>Simplifying carbon and water tracking</li>
            <li>Transforming supply chains for a greener future</li>
          </ul>
        </div>

        {/* What We Do Block */}
        <div className="mt-8">
          <h2 className="text-3xl font-bold text-gray-800">What We Do</h2>
          <ul className="text-lg text-gray-600 mt-4 list-disc pl-6 space-y-2">
            <li>Upload standard BOM</li>
            <li>Calculate carbon emissions</li>
            <li>Track water usage</li>
            <li>Generate sustainability score</li>
            <li>Provide actionable insights</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default About;
