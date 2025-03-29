import Navbar from '../components/Navbar.jsx';
import Hero from '../components/Hero.jsx';
import About from '../components/About.jsx';

function Global() {
  return (
    <>
      <div>
        <Navbar/>
        {/* Add description between Navbar and iframe */}
        <div style={{ textAlign: 'center', margin: '20px 0', fontSize: '18px', color: '#555' }}>
          <p>
            We've aggregated data from over 150 companies worldwide to provide insights through these graphs. Explore the global impact and trends.
          </p>
        </div>
        <iframe
            src="/carbon_heatmap_2024.html"
            title="Carbon Heatmap 2024"
            width="100%"
            height="600px"
            style={{border: 'none'}}
            onError={() => console.error("Error loading the heatmap")}
        />
        <iframe
            src="/water_heatmap_2024.html"
            title="Water Heatmap 2024"
            width="100%"
            height="600px"
            style={{border: 'none'}}
            onError={() => console.error("Error loading the heatmap")}
        />
      </div>
    </>
  );
}

export default Global;