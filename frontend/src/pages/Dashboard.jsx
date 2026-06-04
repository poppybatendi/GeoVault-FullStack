import { useEffect, useState } from "react";

import api from "../api/api";

import MineralChart from "../components/MineralChart";
import SampleTable from "../components/SampleTable";
import DashboardCard from "../components/DashboardCard";
import { Link } from "react-router-dom";

import "./Dashboard.css";
import Navbar from "../components/Navbar";

function Dashboard() {

  const [stats, setStats] = useState({
    samples: 0,
    reports: 0,
    activities: 0
  });

  const [minerals, setMinerals] = useState([]);

  const [insights, setInsights] = useState([]);

  const [portfolioHealth, setPortfolioHealth] =
    useState(null);

  

  useEffect(() => {

    const loadDashboard = async () => {

      try {

        const token =
          localStorage.getItem("token");

        const headers = {
          Authorization: `Bearer ${token}`
        };

        // Dashboard Summary

        const dashboardResponse =
          await api.get(
            "/dashboard",
            { headers }
          );

        setStats(
          dashboardResponse.data
        );

        // Mineral Statistics

        const mineralResponse =
          await api.get(
            "/dashboard/minerals",
            { headers }
          );

        setMinerals(
          mineralResponse.data
        );

        // Portfolio Health

        const healthResponse =
          await api.get(
            "/ai/portfolio-health",
            { headers }
          );

        console.log(
          "Portfolio Health:",
          healthResponse.data
        );

        setPortfolioHealth(
          healthResponse.data
        );

        // Samples

        const samplesResponse =
          await api.get(
            "/my-samples",
            { headers }
          );

        setSamples(
          samplesResponse.data
        );

      } catch (error) {

        console.error(
          "Dashboard Error:",
          error
        );

      }
    };

    loadDashboard();

  }, []);

  return (
    <div>

    <Navbar />

    <div className="dashboard-container">

      {/* KPI CARDS */}

      <div className="stats-row">

        <DashboardCard
          title="Samples"
          value={stats.samples}
        />

        <DashboardCard
          title="Reports"
          value={stats.reports}
        />

        <DashboardCard
          title="Activities"
          value={stats.activities}
        />

      </div>

      {/* CHART + PORTFOLIO */}

      <div className="two-column">

        <div className="card">

          <h2>Mineral Distribution</h2>

          <MineralChart
            data={minerals}
          />

        </div>

        <div className="card">

          <h2>Portfolio Health</h2>

          {portfolioHealth && (

            <>
              <p>
                <strong>Status:</strong>{" "}
                {portfolioHealth.status}
              </p>

              <p>
                <strong>Health Score:</strong>{" "}
                {portfolioHealth.score}
              </p>

              <p>
                <strong>Total Samples:</strong>{" "}
                {portfolioHealth.samples}
              </p>

              <p>
                <strong>Total Reports:</strong>{" "}
                {portfolioHealth.reports}
              </p>

              <p>
                <strong>Samples Without Reports:</strong>{" "}
                {portfolioHealth.samples_without_reports}
              </p>

              <p>
                <strong>Missing Coordinates:</strong>{" "}
                {portfolioHealth.missing_coordinates}
              </p>
            </>

          )}

        </div>        
        </div>

      </div>

    </div>

  );
}

export default Dashboard;