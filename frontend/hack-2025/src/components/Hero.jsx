import React from 'react'
import {Link} from 'react-router-dom'


const Hero = () => {
    return(
        <div className = 'text-black'>
            <div className='max-w-[800px] mt-[-96px] w-full h-screen mx-auto text-center flex flex-col justify-center'>
                <p className='text-black font-bold p-2'>
                    Get reports
                    </p>
                <h1 className='md:text-7xl sm:text-6xl text-4xl font-bold md:py-6'>
                    Make earth better
                    </h1>
                <div className='flex justify-center items-center'>
                    <p className='md:text-5xl sm:text-4xl text-xl font-bold py-4'>
                        some good stuff
                        </p>
                </div>
                <p className= 'md:text-2xl text-xl font-bold text-gray-500'>
                    djkfsjkdlsafjkldas;fjdklasjkdlfjakl; jfdksl;fjdksla;f
                    </p>
                    <div className='flex mx-auto sm:flex-row justify-center items-center gap-4 my-6'>
                        <Link to="/business">
                        <button className='bg-amber-600 w-[200px] rounded-md font-medium my-6 mx-auto py-3 text-black hover:scale-105 transition-all duration-300 ease-in-out'>
                            For Businesses
                            </button>
                        </Link>
                        <Link to="/individual">
                        <button className='bg-amber-950 w-[200px] rounded-md font-medium my-6 mx-auto py-3 text-white hover:scale-105 transition-all duration-300 ease-in-out'>
                            For Individuals
                            </button>
                        </Link>
                    </div>
            </div>
        </div>
    )
}

export default Hero