import { useEffect, useState } from "react";

import {
  MapContainer,
  TileLayer,
  Marker,
  Popup
} from "react-leaflet";

import L from "leaflet";

import api from "../api/api";
import Navbar from "../components/Navbar";

function getMarkerColor(mineral) {

  switch (mineral?.toLowerCase()) {

    case "copper":
      return "orange";

    case "gold":
      return "yellow";

    case "nickel":
      return "green";

    case "lithium":
      return "violet";

    default:
      return "blue";
  }
}

function createIcon(color) {

  return new L.Icon({

    iconUrl:
      `https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-${color}.png`,

    shadowUrl:
      "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",

    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34]

  });
}

function MapView() {

  const [samples, setSamples] =
    useState([]);

  const [selectedMineral, setSelectedMineral] =
  useState("All");

  useEffect(() => {

    const loadSamples = async () => {

      try {

        const token =
          localStorage.getItem("token");

        const response =
          await api.get(
            "/my-samples",
            {
              headers: {
                Authorization:
                  `Bearer ${token}`
              }
            }
          );

        setSamples(
          response.data
        );

      } catch (error) {

        console.error(
          "Map Error:",
          error
        );

      }
    };

    loadSamples();

  }, []);

  const filteredSamples =

  selectedMineral === "All"

    ? samples

    : samples.filter(

        sample =>

          sample.mineral ===
          selectedMineral

      );

      const minerals = [

      "All",

      ...new Set(
        samples.map(
          sample => sample.mineral
        )
      )

    ];
    
     return (

  <div>

    <Navbar />

    <div
      style={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        marginBottom: "20px"
      }}
    >

      <h1>Exploration Map</h1>

      <div>

        <label>
          <strong>Filter Mineral:</strong>
        </label>

        <select
          value={selectedMineral}
          onChange={(e) =>
            setSelectedMineral(
              e.target.value
            )
          }
          style={{
            marginLeft: "10px",
            padding: "8px"
          }}
        >

          {minerals.map((mineral) => (

            <option
              key={mineral}
              value={mineral}
            >
              {mineral === "All"
                ? "All Minerals"
                : mineral}
            </option>

          ))}

        </select>

      </div>

    </div>
    
      <MapContainer
        center={[-22.3285, 24.6849]}
        zoom={6}
        style={{
          height: "600px",
          width: "100%"
        }}
      >

        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {filteredSamples.map(sample => (

          sample.latitude &&
          sample.longitude && (

           <Marker
              key={sample.id}
              position={[
                sample.latitude,
                sample.longitude
              ]}
              icon={
                createIcon(
                  getMarkerColor(
                    sample.mineral
                  )
                )
              }
            >
            
            <Popup>

                <h3>{sample.mineral}</h3>

                <p>
                <strong>Depth:</strong>{" "}
                {sample.depth} m
                </p>

                <p>
                <strong>Risk:</strong>{" "}
                {sample.risk_level}
                </p>

                <p>
                <strong>Latitude:</strong>{" "}
                {sample.latitude}
                </p>

                <p>
                <strong>Longitude:</strong>{" "}
                {sample.longitude}
                </p>

            </Popup>
            </Marker>

          )

        ))}

      </MapContainer>

       <div className="card">

      <h3>Mineral Legend</h3>

      <p>🟠 Copper</p>
      <p>🟡 Gold</p>
      <p>🟢 Nickel</p>
      <p>🟣 Lithium</p>
      <p>🔵 Other</p>

    </div>

    </div>

  );
}

export default MapView;