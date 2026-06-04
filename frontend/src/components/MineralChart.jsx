import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend
} from "chart.js";

import { Pie } from "react-chartjs-2";

ChartJS.register(
  ArcElement,
  Tooltip,
  Legend
);

function MineralChart({ data }) {

 const chartData = {
  labels: data.map(item => item.mineral),
  datasets: [
    {
      data: data.map(item => item.count),

      backgroundColor: [
        "#3b82f6",
        "#10b981",
        "#f59e0b",
        "#ef4444",
        "#8b5cf6",
        "#06b6d4",
        "#84cc16"
      ]
    }
  ]
};

  return (

  <div
    style={{
      width: "350px",
      height: "250px",
      margin: "0 auto"
    }}
  >

    <Pie
      data={chartData}
      options={{
        maintainAspectRatio: false
      }}
    />

  </div>

);
}

export default MineralChart;