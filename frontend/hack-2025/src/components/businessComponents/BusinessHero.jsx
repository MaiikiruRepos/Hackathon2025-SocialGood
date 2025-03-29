import React, {useCallback} from 'react'
import business from '/src/assets/business.jpg';
import DropzoneUpload from './DropzoneUpload'



const BusinessHero = () => {
    return (
        <div className='w-full bg-white py-16 px-4'>
            <div className='max-w-[1240px] mx-auto grid md:grid-cols-2'>
                <img className='w-[500px] mx-auto my-4'src={business} alt="/Business" />
                <div className='flex flex-col justify-center'>
                    <p className='text-black uppercase font-bold'>Header</p>
                    <h1 className='md:texxt-4xl sm:text-3xl text-2xl font-bold py-2'>What we do </h1>
                    <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. 
                        Voluptatem in commodi qui. Saepe, fugiat sit! Ullam, dolor natus. Aspernatur eveniet inventore 
                        debitis sequi quis pariatur aut et alias assumenda aliquid?
                        </p>
                      <DropzoneUpload/>
                </div>
            </div>
        </div>
    )
}

export default BusinessHero