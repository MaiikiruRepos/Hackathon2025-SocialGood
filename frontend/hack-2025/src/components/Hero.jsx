import React from 'react'
import { Link } from 'react-router-dom'
import { FiChevronDown } from 'react-icons/fi'
import forest from '/src/assets/forest.jpg' // use your actual image path

const Hero = () => {
  return (
    <div
      className="w-full bg-cover bg-center bg-no-repeat"
      style={{ backgroundImage: `url(${forest})` }}
    >
      <div className="w-full bg-black/60 px-4 py-24">
        <div className="max-w-[1240px] mx-auto text-center text-white px-8">
          <p className="text-[#A0FEC0] font-bold text-2xl">Get reports</p>
          <h1 className="md:text-7xl sm:text-6xl text-4xl font-bold md:py-4">
            Make earth better
          </h1>
          <p className="md:text-2xl text-xl font-medium text-gray-200">
            some good stuff
          </p>
          <p className="md:text-xl text-lg font-light text-gray-300 mt-4">
            djkfsjkdlsafjkldas;fjdklasjkdlfjakl; jfdksl;fjdksla;f
          </p>

          <div className="flex flex-col sm:flex-row justify-center items-center gap-4 mt-10">
            <Link to="/business">
              <button className="bg-white text-[#1A1A1A] w-[200px] rounded-md font-medium py-3 hover:scale-105 transition-all duration-300 ease-in-out">
                For Businesses
              </button>
            </Link>
            <Link to="/individual">
              <button className="bg-[#00A86B] text-[#1A1A1A] w-[200px] rounded-md font-medium py-3 hover:scale-105 transition-all duration-300 ease-in-out">
                For Individuals
              </button>
            </Link>
          </div>

          <p className="text-gray-300 mt-10">Scroll for more information</p>
          <div className="mt-4 flex justify-center">
            <FiChevronDown className="text-3xl text-white animate-bounce" />
          </div>
        </div>
      </div>
    </div>
  )
}

export default Hero
