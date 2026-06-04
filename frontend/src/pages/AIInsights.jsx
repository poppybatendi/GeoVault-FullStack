import { useEffect, useState } from "react";

import api from "../api/api";
import Navbar from "../components/Navbar";

function AIInsights() {

  const [insights, setInsights] =
    useState([]);

  const [executiveBriefing,
    setExecutiveBriefing] =
    useState(null);

  useEffect(() => {

    const loadAI = async () => {

      try {

        const token =
          localStorage.getItem("token");

        const headers = {
          Authorization:
            `Bearer ${token}`
        };

        const insightsResponse =
          await api.get(
            "/ai/insights",
            { headers }
          );

        setInsights(
          insightsResponse.data.insights
        );

        const briefingResponse =
          await api.get(
            "/ai/executive-briefing",
            { headers }
          );

        setExecutiveBriefing(
          briefingResponse.data
        );

      } catch (error) {

        console.error(
          "AI Error:",
          error
        );

      }
    };

    loadAI();

  }, []);

  return (

    <div>

      <Navbar />

      <h1>
        AI Intelligence Center
      </h1>

      <div className="card">

        <h2>AI Insights</h2>

        <ul>

          {insights.map(
            (item, index) => (

              <li key={index}>
                {item}
              </li>

            )
          )}

        </ul>

      </div>

      {executiveBriefing && (

        <div className="card">

          <h2>
            Executive Briefing
          </h2>

          <p>
            <strong>
              Overview
            </strong>
            <br />
            {executiveBriefing.overview}
          </p>

          <p>
            <strong>
              Risks
            </strong>
            <br />
            {executiveBriefing.risks}
          </p>

          <p>
            <strong>
              Opportunities
            </strong>
            <br />
            {executiveBriefing.opportunities}
          </p>

          <p>
            <strong>
              Recommendations
            </strong>
            <br />
            {executiveBriefing.recommendations}
          </p>

        </div>

      )}

    </div>

  );
}

export default AIInsights;