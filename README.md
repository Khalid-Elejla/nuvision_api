# Traffic Analysis SaaS with YOLO

This project is a SaaS application for traffic analysis based on the YOLO algorithm. It includes user authentication, project management, location management, and video analysis. The frontend is built with Next.js 13, and the backend is built with FastAPI. The backend handles user login, project management, location management, and video management. Each project can contain multiple locations, and each location can contain multiple videos to be analyzed.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Database Models](#database-models)
- [Testing](#testing)

## Features

- User authentication and authorization
- Project management (create, read, update, delete)
- Location management within projects (create, read, update, delete)
- Video management within locations (create, read, update, delete)
- YOLO-based video analysis

## Installation

### Prerequisites

- Python 3.8+
- Node.js 14+
- FastAPI
- SQLAlchemy
- Uvicorn
- Next.js
- Docker (optional, for containerization)

### Backend Setup

1. **Clone the repository:**

   ```sh
   git clone https://github.com/yourusername/traffic-analysis-saas.git
   cd traffic-analysis-saas/backend
