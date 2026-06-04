import { useEffect, useState } from "react";

import api from "../api/api";
import Navbar from "../components/Navbar";

function Reports() {

  const [reports, setReports] =
    useState([]);

  const downloadReport = async (
    reportId,
    filename
  ) => {

    const token =
      localStorage.getItem("token");

    const response =
      await api.get(
        `/reports/${reportId}/download`,
        {
          responseType: "blob",
          headers: {
            Authorization:
              `Bearer ${token}`
          }
        }
      );

    const url =
      window.URL.createObjectURL(
        new Blob(
          [response.data],
          {
            type: "application/pdf"
          }
        )
      );

    const link =
      document.createElement("a");

    link.href = url;

    link.setAttribute(
      "download",
      filename
    );

    document.body.appendChild(link);

    link.click();

  };

  useEffect(() => {

    const loadReports = async () => {

      try {

        const token =
          localStorage.getItem("token");

        const response =
          await api.get(
            "/reports",
            {
              headers: {
                Authorization:
                  `Bearer ${token}`
              }
            }
          );

        setReports(
          response.data
        );

      } catch (error) {

        console.error(error);

      }

    };

    loadReports();

  }, []);

  return (

    <div>

      <Navbar />

      <h1>
        Reports
      </h1>

      <table
        border="1"
        cellPadding="8"
      >

        <thead>

          <tr>
            <th>ID</th>
            <th>Title</th>
            <th>Filename</th>
            <th>Sample ID</th>
            <th>Actions</th>
          </tr>

        </thead>

        <tbody>

          {reports.map(report => (

            <tr
              key={report.id}
            >

              <td>{report.id}</td>

              <td>
                {report.title}
              </td>

              <td>
                {report.filename}
              </td>

              <td>
                {report.sample_id}
              </td>
               <td>

               <button
                onClick={() =>
                  downloadReport(
                    report.id,
                    report.filename
                  )
                }
              >
                Download
              </button>

            </td>

            </tr>

          ))}

        </tbody>

      </table>

    </div>

  );

}

export default Reports;