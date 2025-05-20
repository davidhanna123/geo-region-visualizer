
const map = L.map('map').setView([20, 10], 2);

// Add OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Load your GeoJSON file
fetch('data/bishops_regions.geojson')
  .then(response => response.json())
  .then(geojson => {
    function onEachFeature(feature, layer) {
      // Add hover popup content
      if (feature.properties) {
        layer.bindPopup(`<b>Bishop:</b> ${feature.properties.bishop}<br/><b>Region:</b> ${feature.properties.region}`);
      }
      layer.on({
        mouseover: (e) => {
          e.target.setStyle({fillOpacity: 0.7});
        },
        mouseout: (e) => {
          geojsonLayer.resetStyle(e.target);
        }
      });
    }

    const geojsonLayer = L.geoJSON(geojson, {
      style: {
        color: '#311b92',
        fillColor: '#6a51a3',
        weight: 2,
        fillOpacity: 0.5
      },
      onEachFeature: onEachFeature
    }).addTo(map);
  });
