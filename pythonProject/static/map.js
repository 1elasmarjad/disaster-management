const mapCenter = [37.0902, -95.7129]; // USA

const map = L.map("map").setView(mapCenter, 5);

L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution:
    '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
}).addTo(map);

// fetch all data from the API

const earthquakeIcon = L.icon({
  iconUrl: "/static/explosion.png", // icon from https://www.flaticon.com/free-icon/explosion_616500?term=explosion&page=1&position=6&origin=tag&related_id=616500
  iconSize: [15, 15],
});

const flameIcon = L.icon({
  iconUrl: "/static/flame.png", // icon from https://www.flaticon.com/free-icon/flame_426833?term=flame&page=1&position=1&origin=tag&related_id=426833
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
    data.disasters.forEach((disaster) => {
      const coord = disaster.geometry.coordinates;
      const lat = coord[1];
      const lon = coord[0];

      if (disaster.type === "earthquake") {
        L.marker([lat, lon], { icon: earthquakeIcon })
          .addTo(map)
          .bindPopup("Magnitude: " + disaster.metadata.mag);
      } else if (disaster.type === "wildfire") {
        L.marker([lat, lon], { icon: flameIcon })
          .addTo(map)
          .bindPopup(disaster.metadata.title);
      }
    });
  });
