📜 Lab Operations Management System
===================================

A vendor-agnostic platform that centralizes instrument data and tracks maintenance costs across all lab equipment. This system provides clear visibility into equipment expenses and ensures maintenance schedules are never missed.

🛠 Tech Stack
-------------

*   **Frontend:** React + Vite
    
*   **Backend:** FastAPI (Python)
    
*   **Database:** PostgreSQL 15
    
*   **Infrastructure:** Docker & Docker Compose
    
*   **DB Management:** pgAdmin 4
    

🚀 Getting Started
------------------

You do **not** need to install PostgreSQL or Python on your local machine. Everything is pre-configured to run inside Docker containers.

### 1\. Clone the repository

git clone https://github.com/Code-A-187/lab\_operations.git

cd lab\_operations

### 2\. Configure Environment Variables

Copy the example environment file and fill in your preferred credentials:

cp .env.example .env

> **Note:** Open the .env file to customize your passwords. These values are used by both Docker and the FastAPI server to establish a secure database connection.

### 3\. Launch the Application

docker-compose up --build

🗄 Database Setup (pgAdmin)
---------------------------

The database lab\_db is created automatically on startup. To browse your tables via the UI:

1.  Open **pgAdmin** at http://localhost:5050.
    
2.  Login with the credentials set in your .env.
    
3.  **Register a New Server:**
    
    *   **Name:** Lab\_System
        
    *   **Connection Tab > Host:** db
        
    *   **Port:** 5432
        
    *   **Username/Password:** Use the values defined in your .env.
        
4.  Navigate to: Servers > Lab\_System > Databases > lab\_db > Schemas > public > Tables.
    

🔗 Service Map
--------------

*   **Frontend:** http://localhost:3000 (The React user interface)
    
*   **Backend API:** http://localhost:8000 (The FastAPI base URL)
    
*   **API Documentation:** http://localhost:8000/docs (Interactive Swagger UI for testing endpoints)
    
*   **Database Management:** http://localhost:5050 (pgAdmin 4 dashboard)

🧪 Development Workflow
-----------------------

*   **Hot Reloading:** The server/ and client/ folders are mounted as Docker volumes. Changes made of local code reflect instantly inside the containers.
    
*   **Database Persistence:** All data is stored in a named volume (postgres\_data), so your data remains safe even if containers are stopped.
