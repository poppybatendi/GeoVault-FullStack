import { useEffect, useState } from "react";

import api from "../api/api";
import Navbar from "../components/Navbar";
import SampleTable from "../components/SampleTable";
import "./Samples.css";

function Samples() {

  const [samples, setSamples] =
    useState([]);

  const handleDelete = (sampleId) => {

    setSamples(prev =>
      prev.filter(
        sample => sample.id !== sampleId
      )
    );

  };

  const [file, setFile] =
  useState(null);
  
  const [reportFile, setReportFile] =
    useState(null);

  const [selectedSample, setSelectedSample] =
    useState("");

  const [reportTitle, setReportTitle] =
    useState("");

  const [searchMineral, setSearchMineral] =
  useState("");

  const [searchLocation, setSearchLocation] =
  useState("");

  const [stats, setStats] = useState({
  samples: 0,
  reports: 0,
  activities: 0
  });
 
  const handleSearch = async () => {

    try {

      const response =
        await api.get(
          "/samples/search",
          {
            params: {
              mineral: searchMineral,
              location: searchLocation
            }
          }
        );

      setSamples(
        response.data
      );

    } catch (error) {

      console.error(
        error
      );
    }
  };

  const handleUpload = async () => {

    if (!file) {
      alert("Select a CSV file");
      return;
    }

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
          error
        );

      }
    };

    loadSamples();

  }, []);

    try {

      const token =
        localStorage.getItem("token");

      const formData =
        new FormData();

      formData.append(
        "file",
        file
      );

      const response =
        await api.post(
          "/samples/import",
          formData,
          {
            headers: {
              Authorization:
                `Bearer ${token}`,
              "Content-Type":
                "multipart/form-data"
            }
          }
        );

      alert(
        response.data.message
      );

    } catch (error) {

      console.error(
        error
      );

      alert(
        "Import failed"
      );
    }
  };

  const handleReportUpload = async () => {

    if (
      !reportTitle ||
      !selectedSample ||
      !reportFile
    ) {

      alert(
        "Please complete all fields"
      );

      return;
    }

    try {

      const token =
        localStorage.getItem("token");

      const formData =
        new FormData();

      formData.append(
        "title",
        reportTitle
      );

      formData.append(
        "sample_id",
        selectedSample
      );

      formData.append(
        "file",
        reportFile
      );

      const response =
        await api.post(
          "/reports/upload",
          formData,
          {
            headers: {
              Authorization:
                `Bearer ${token}`,
              "Content-Type":
                "multipart/form-data"
            }
          }
        );

      alert(
        response.data.message
      );

    } catch (error) {

      console.error(
        error
      );

      alert(
        "Report upload failed"
      );
    }
  };

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
          "Samples Error:",
          error
        );

      }
    };

    loadSamples();

  }, []);

  return (

    <div>

      <Navbar />

      <h1>
        Geological Samples
      </h1>

      <div className="card">

      <h3>
        Import Samples CSV
      </h3>

        <input
          type="file"
          accept=".csv"
          onChange={(e) =>
            setFile(
              e.target.files[0]
            )
          }
        />

        <button
          onClick={handleUpload}
        >
          Upload CSV
        </button>

      </div>

      <div className="card">

    <h3>
      Upload Exploration Report
    </h3>

    <input
      type="text"
      placeholder="Report Title"
      value={reportTitle}
      onChange={(e) =>
        setReportTitle(
          e.target.value
        )
      }
    />

    <br />
    <br />

    <select
      value={selectedSample}
      onChange={(e) =>
        setSelectedSample(
          e.target.value
        )
      }
    >

      <option value="">
        Select Sample
      </option>

      {samples.map(sample => (

        <option
          key={sample.id}
          value={sample.id}
        >

          {sample.mineral}
          {" - "}
          {sample.location}

        </option>

      ))}

    </select>

    <br />
    <br />

    <input
      type="file"
      accept=".pdf,.doc,.docx"
      onChange={(e) =>
        setReportFile(
          e.target.files[0]
        )
      }
    />

    <br />
    <br />

    <button
      onClick={
        handleReportUpload
      }
    >
      Upload Report
    </button>

    </div>
        
        <div className="card">

    <h3>
      Search Samples
    </h3>

    <input
      type="text"
      placeholder="Mineral"
      value={searchMineral}
      onChange={(e) =>
        setSearchMineral(
          e.target.value
        )
      }
    />

    <input
      type="text"
      placeholder="Location"
      value={searchLocation}
      onChange={(e) =>
        setSearchLocation(
          e.target.value
        )
      }
    />

    <button
      onClick={handleSearch}
    >
      Search
    </button>

  </div>
      <div className="table-header">
        <h3>
          Samples ({samples.length})
        </h3>

      </div>
      <SampleTable
        samples={samples}
        onDelete={handleDelete}
      />

    </div>

  );
}

export default Samples;