import React from 'react'
import business from '/src/assets/business.jpg';


const BusinessHero = () => {
    return (
        <div className='w-full bg-white py-16 px-4'>
            <div className='max-w-[1240px] mx-auto grid md:grid-cols-2'>
                <img src={business} alt="/Business" />
                <div>
                    <p>Header</p>
                    <h1>What we do </h1>
                    <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. 
                        Voluptatem in commodi qui. Saepe, fugiat sit! Ullam, dolor natus. Aspernatur eveniet inventore 
                        debitis sequi quis pariatur aut et alias assumenda aliquid?</p>
                </div>
            </div>
        </div>
    )
}

export default BusinessHero