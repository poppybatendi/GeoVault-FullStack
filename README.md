# GeoVault Full Stack Application

## Overview

GeoVault is a full-stack geological exploration management platform designed to help exploration teams manage geological samples, exploration reports, geospatial data, and AI-powered insights.

The application provides secure user authentication, sample management, document storage, map visualization, activity tracking, and intelligent exploration analysis through a modern web interface.

---

## Features

### Authentication & Security

* User registration
* User login
* JWT authentication
* Protected API endpoints
* User-specific data access

### Geological Sample Management

* Create geological samples
* View geological samples
* Update geological samples
* Delete geological samples
* Search samples by mineral and location
* Import samples from CSV files

### Exploration Report Management

* Upload exploration reports
* Associate reports with samples
* Download reports
* View reports by sample
* Track report ownership

### Mapping & Geospatial Analysis

* Interactive map visualization
* Sample location plotting
* Sample popup details
* Nearby sample search
* Geographic filtering
* GeoJSON support

### Activity Tracking

* User activity logging
* Audit trail
* Activity history dashboard

### AI-Powered Insights

* Sample summaries
* Risk assessments
* Opportunity scoring
* Exploration insights
* Executive briefings
* Portfolio health scoring
* High-priority target identification
* Exploration hotspot detection
* Narrative reporting

### Dashboard & Analytics

* Sample statistics
* Mineral distribution analysis
* Report statistics
* Activity summaries
* AI-generated recommendations

---

## System Architecture

Frontend (React + Vite)

↓

REST API (Flask)

↓

SQLAlchemy ORM

↓

PostgreSQL Database

↓

File Storage (Exploration Reports)

---

## Technology Stack

### Frontend

* React
* Vite
* Axios
* React Router
* Leaflet Maps

### Backend

* Python
* Flask
* Flask JWT Extended
* SQLAlchemy
* PostgreSQL

### DevOps & Tools

* Docker
* Git
* GitHub

---

## Project Structure

GeoVault-FullStack/

├── backend/

│ ├── models/

│ ├── routes/

│ ├── utils/

│ └── app.py

│

├── frontend/

│ ├── src/

│ ├── components/

│ ├── pages/

│ └── api/

│

└── README.md

---

## Screenshots

### Login Page

<img width="300" height="265" alt="image" src="https://github.com/user-attachments/assets/0c471d24-8374-49d7-add1-74ebd721b3f2" />

### Dashboard

<img width="975" height="431" alt="image" src="https://github.com/user-attachments/assets/e44ca1d2-a021-4054-aa5b-1e4b1f97da38" />

### Samples Management and AI Summary Modal

<img width="975" height="433" alt="image" src="https://github.com/user-attachments/assets/c0a7d0d7-9ce0-46b2-aae9-672b3542be74" />

### Reports Management

<img width="975" height="165" alt="image" src="https://github.com/user-attachments/assets/89f84227-2b34-49cd-a4b3-45363b78472a" />

### Interactive Map

<img width="975" height="429" alt="image" src="https://github.com/user-attachments/assets/e287c966-0163-46f7-a311-581768573b79" />

### AI Insights

<img width="975" height="416" alt="image" src="https://github.com/user-attachments/assets/e13904dc-05aa-4b8d-b41d-996aef440867" />


---

## Installation

### Clone Repository

git clone https://github.com/poppybatendi/GeoVault-FullStack.git

cd GeoVault-FullStack

### Backend Setup

cd backend

pip install -r requirements.txt

python app.py

### Frontend Setup

cd frontend

npm install

npm run dev

---

## API Highlights

### Authentication

POST /register

POST /login

### Samples

GET /samples

POST /samples

PUT /samples/<id>

DELETE /samples/<id>

### Reports

POST /reports/upload

GET /reports

GET /reports/<id>/download

### AI Services

POST /ai/sample-summary/<id>

GET /ai/risk-assessment/<id>

GET /ai/opportunity-score/<id>

GET /ai/insights

GET /ai/executive-briefing

GET /ai/portfolio-health

---

## Future Enhancements

* Advanced geological reporting
* PDF report generation
* Machine learning mineral prediction
* Role-based access control
* Cloud storage integration
* Mobile application
* Dark mode support
* Advanced map clustering
* Real-time collaboration

---

## Author

Poppy Batendi

Full Stack Developer

GitHub: https://github.com/poppybatendi
