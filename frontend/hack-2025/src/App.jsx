
import {Routes, Route} from 'react-router-dom'
import Navbar from './components/Navbar'
import Home from './pages/Home';
import Business from './pages/Business';
import Individual from './pages/Individual';
import Dashboard from './pages/Dashboard';
import './index.css'


function App() {

  return (
    <>
      <div>
        <Routes>
          <Route path="/" element={<Home/>} />
          <Route path="/business" element={<Business />} />
          <Route path="/individual" element={<Individual />} />
          <Route path="/dashboard" element={<Dashboard />} />
        </Routes>
      </div>
    </>
  )
}

export default App
