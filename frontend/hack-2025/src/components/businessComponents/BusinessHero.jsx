import React, {useCallback} from 'react'
import business from '/src/assets/business.jpg';
import DropzoneUpload from './DropzoneUpload'



const BusinessHero = () => {
    return (
        <div className='w-full bg-white py-16 px-4'>
            <div className='max-w-[1240px] mx-auto grid md:grid-cols-2'>
                <img className='w-[500px] mx-auto my-4'src={business} alt="/Business" />
                <div className='flex flex-col justify-center'>
                    <p className='text-black uppercase font-bold'>Improve the world</p>
                    <h1 className='md:texxt-4xl sm:text-3xl text-2xl font-bold py-2'>How it works: </h1>
                    <p> Please upload a .zip of all your BOM information so that we can process your information and give you an estimate of your footprint on the world.
                        </p>
                      <DropzoneUpload/>
                </div>
            </div>
        </div>
    )
}

export default BusinessHero