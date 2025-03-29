import React, { useState } from 'react';
import { AiOutlineClose, AiOutlineMenu } from 'react-icons/ai';
import { Link } from 'react-router-dom';

const Navbar = () => {
  const [nav, setNav] = useState(false);

  const handleNav = () => {
    setNav(!nav);
  };

  return (
    <div className='sticky top-0 z-50 shadow-sm bg-[#1A1A1A]'>
      <div className='flex justify-between items-center h-24 max-w-[1240px] mx-auto px-4 text-white'>
        {/* Make "Ecopulse." clickable and route to home page */}
        <Link to="/" className='w-full text-3xl font-bold text-[#00A86B]'>
          Ecopulse.
        </Link>

        <ul className='hidden md:flex'>
          <li className='p-4 hover:underline underline-offset-4 cursor-pointer font-semibold'>
            <Link to="/">Home</Link>
          </li>
          <li className='p-4 hover:underline underline-offset-4 cursor-pointer font-semibold'>
            <Link to="/business">Businesses</Link>
          </li>
          <li className='p-4 hover:underline underline-offset-4 cursor-pointer font-semibold'>
            <Link to="/global">Global</Link>
          </li>
          <li className='p-4 hover:underline underline-offset-4 cursor-pointer font-semibold'>
            <Link to="/dashboard">Dashboard</Link>
          </li>
        </ul>

        <div onClick={handleNav} className='block md:hidden'>
          {nav ? <AiOutlineClose size={20}/> : <AiOutlineMenu size={20} />}
        </div>

        <ul className={nav ? 'fixed left-0 top-0 w-[60%] h-full border-r border-r-gray-900 bg-amber-50 ease-in-out duration-500' : 'ease-in-out duration-500 fixed left-[-100%]'}>
          <h1 className='w-full text-3xl font-bold text-black m-4'>
            <Link to="/" onClick={handleNav}>Ecopulse.</Link>
          </h1>
          <li className='p-4 border-b border-gray-600'>
            <Link to="/" onClick={handleNav}>Home</Link>
          </li>
          <li className='p-4 border-b border-gray-600'>
            <Link to="/business" onClick={handleNav}>Business</Link>
          </li>
          <li className='p-4 border-b border-gray-600'>
            <Link to="/global" onClick={handleNav}>Global</Link>
          </li>
          <li className='p-4 '>
            <Link to="/dashboard" onClick={handleNav}>Dashboard</Link>
          </li>
        </ul>
      </div>
    </div>
  );
};

export default Navbar;
