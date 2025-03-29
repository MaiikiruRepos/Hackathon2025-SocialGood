import Navbar from '../components/Navbar.jsx';

function Global() {
  return (
    <>
      <div className="min-h-screen bg-[#F7F8F9] text-[#1A1A1A]">
        <Navbar />

        {/* Intro Section */}
        <div className="max-w-[1240px] mx-auto px-6 py-12 text-center">
          <h1 className="text-4xl font-bold mb-4 text-[#00A86B]">Global Sustainability Insights</h1>
          <p className="text-lg text-gray-700 max-w-2xl mx-auto">
            We've aggregated data from over <strong>150 companies</strong> worldwide to provide 
            insights into carbon and water usage. Explore how different regions are impacting — 
            and improving — the planet.
          </p>
        </div>

        {/* Chart Containers */}
        <div className="max-w-[1240px] mx-auto px-4 grid gap-12">
          {/* Carbon Map */}
          <div className="bg-white rounded-xl shadow-lg overflow-hidden">
            <h2 className="text-2xl font-semibold px-6 pt-6 pb-2">Carbon Emissions Heatmap</h2>
            <iframe
              src="/carbon_heatmap_2024.html"
              title="Carbon Heatmap 2024"
              width="100%"
              height="600px"
              style={{ border: 'none' }}
              onError={() => console.error("Error loading the heatmap")}
            />
          </div>

          {/* Water Map */}
          <div className="bg-white rounded-xl shadow-lg overflow-hidden">
            <h2 className="text-2xl font-semibold px-6 pt-6 pb-2">Water Usage Heatmap</h2>
            <iframe
              src="/water_heatmap_2024.html"
              title="Water Heatmap 2024"
              width="100%"
              height="600px"
              style={{ border: 'none' }}
              onError={() => console.error("Error loading the heatmap")}
            />
          </div>
        </div>

        {/* Footer spacing */}
        <div className="py-12" />
      </div>
    </>
  );
}

export default Global;
