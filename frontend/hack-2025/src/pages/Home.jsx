import { useState } from 'react'
import Navbar from '../components/Navbar.jsx'
import '../index.css'
import Hero from '../components/hero.jsx'
import About from '../components/About.jsx'


function Home() {

  return (
    <>
      <div>
        <Navbar />
        <Hero />
        <About />
      </div>
    </>
  )
}

export default Home
