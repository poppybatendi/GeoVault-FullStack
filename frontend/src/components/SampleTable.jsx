import { useState } from "react";
import api from "../api/api";

function SampleTable({ samples, onDelete }) {

    const [summaryData, setSummaryData] =
    useState(null);

    const [showSummary, setShowSummary] =
      useState(false);

    const deleteSample = async (sampleId) => {

    const confirmed = window.confirm(
      "Delete this sample?\n\n" +
      "This action cannot be undone.\n\n" +
      "All associated reports/documents will also be permanently deleted."
    );

    if (!confirmed) {
      return;
    }

    try {

      const token =
        localStorage.getItem("token");

      await api.delete(
        `/samples/${sampleId}`,
        {
          headers: {
            Authorization:
              `Bearer ${token}`
          }
        }
      );

      alert("Sample deleted successfully");

      onDelete(sampleId);

    } catch (error) {

      console.error(error);

      alert("Failed to delete sample");

    }

  };

  const generateSummary =
    async (sampleId) => {

      try {

        const token =
          localStorage.getItem("token");

        const response =
          await api.post(
            `/ai/sample-summary/${sampleId}`,
            {},
            {
              headers: {
                Authorization:
                  `Bearer ${token}`
              }
            }
          );

        setSummaryData(
         response.data
        );

        setShowSummary(true);

      } catch (error) {

        console.error(error);

      }
    };

  return (

    <>
      <table
        border="1"
        cellPadding="8"
      >

        <thead>
          <tr>
            <th>ID</th>
            <th>Mineral</th>
            <th>Location</th>
            <th>Depth</th>
            <th>Actions</th>
          </tr>
        </thead>

        <tbody>

          {samples.map(sample => (

            <tr key={sample.id}>

              <td>{sample.id}</td>

              <td>{sample.mineral}</td>

              <td>{sample.location}</td>

              <td>{sample.depth_meters}</td>

              <td>

              <button
                onClick={() =>
                  generateSummary(sample.id)
                }
              >
                AI Summary
              </button>

              <button
                onClick={() =>
                  deleteSample(sample.id)
                }
              >
                Delete
              </button>

            </td>

            </tr>

          ))}

        </tbody>

      </table>

       {showSummary && (

      <div
        style={{
          position: "fixed",
          top: 0,
          left: 0,
          width: "100%",
          height: "100%",
          backgroundColor: "rgba(0,0,0,0.5)",
          display: "flex",
          justifyContent: "center",
          alignItems: "center"
        }}
      >

        <div
          style={{
            backgroundColor: "white",
            padding: "20px",
            borderRadius: "10px",
            width: "700px",
            maxWidth: "90%"
          }}
        >

          <h2>
            AI Geological Summary
          </h2>

          <div>

            <h3>
              {summaryData?.mineral}
            </h3>

            <p>
              <strong>Location:</strong>{" "}
              {summaryData?.location}
            </p>

            <p>
              <strong>Depth:</strong>{" "}
              {summaryData?.depth}m
            </p>

            <p>
              <strong>Reports Attached:</strong>{" "}
              {summaryData?.report_count}
            </p>

            <hr />

            <p>
              <strong>Risk Level:</strong>{" "}
              {summaryData?.risk_level}
            </p>

            <p>
              <strong>Opportunity Score:</strong>{" "}
              {summaryData?.opportunity_score}/100
            </p>

            <hr />

            <p>
              <strong>Recommendation</strong>
            </p>

            <p>
              {summaryData?.recommendation}
            </p>

            <hr />

            <p>
              <strong>AI Summary</strong>
            </p>

            <p>
              {summaryData?.summary}
            </p>

          </div>

          <button
            onClick={() =>
              setShowSummary(false)
            }
          >
            Close
          </button>

        </div>

      </div>
       )}
    </>
  );
}


export default SampleTable;