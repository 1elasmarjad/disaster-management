const mapCenter = [37.0902, -95.7129]; // USA

const map = L.map("map").setView(mapCenter, 4);

L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution:
    '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
}).addTo(map);

// fetch all data from the API

const earthquakeIcon = L.icon({
  iconUrl: "/static/explosion.png", // icon from https://www.flaticon.com/free-icons/explosion
  iconSize: [15, 15],
});

fetch("/api/data")
  .then((resp) => {
    if (!resp.ok) {
      throw new Error("Failed to fetch data");
    }

    return resp.json();
  })
  .then((data) => {
    console.log(data);

    data.features.forEach((feature) => {
      const coord = feature.geometry.coordinates;
      const lat = coord[1];
      const lon = coord[0];

      console.log(feature);

      L.marker([lat, lon], { icon: earthquakeIcon })
        .addTo(map)
        .bindPopup("Magnitude: " + feature.metadata.mag);
    });
  });
