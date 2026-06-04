import { Link } from "react-router-dom";
import "./Navbar.css";

function Navbar() {

  return (

    <nav className="navbar">

      <h2>GeoVault</h2>

      <div className="nav-links">

        <Link to="/dashboard">
          Dashboard
        </Link>

        <Link to="/map">
          Map
        </Link>

        <Link to="/samples">
          Samples
        </Link>

        <Link to="/ai">
          AI Insights
        </Link>

        <Link to="/reports">
          Reports
        </Link>

      </div>

    </nav>

  );
}

export default Navbar;