# Docker Compose Config for App

## Services
- `authentication`
    - Description: Authentication service for user authentication.
    - Image: Built from the Dockerfile in the ./authentication directory.
    - Container Name: authentication
    - Network: app-network
    - Restart Policy: Always
- `enter-data`
    - Description: Service for entering temperature data into the MySQL database.
    - Image: Built from the Dockerfile in the ./enter-data directory.
    - Container Name: enter-data
    - Network: app-network
    - Restart Policy: Always
    - Ports: Exposes port 5000 on the host and maps it to port 5000 in the container.
    - Environment Variables:
        - MYSQL_HOST: Hostname of the MySQL database service (mysql-db).
        - MYSQL_PASSWORD: MySQL root password.
        - AUTH_URL: URL of the authentication service (http://- authentication:3000).
    - Dependencies: Depends on the mysql-db service.
- `show-results`
    - Description: Service for displaying temperature data from MongoDB.
    - Image: Built from the Dockerfile in the ./show-results directory.
    - Container Name: show-results
    - Network: app-network
    - Restart Policy: Always
    - Environment Variables:
        - MONGO_HOST: Hostname of the MongoDB service (mongo).
        - MONGO_PORT: MongoDB port (27017).
        - Dependencies: Depends on the mongo service.
- `analytics`
    - Description: Service for providing temperature analytics.
    - Image: Built from the Dockerfile in the analytics directory.
    - Container Name: analytics
    - Network: app-network
## Networks
- `app-network`
   - Description: Custom bridge network for connecting the services within the application stack.
    - Driver: Bridge

# Authentication
## Prerequisites
- Node.js

## Usage

The application will listen to http://localhost:3000 

## API Endpoint

Takes post request to `/` which expects a JSON request body:
`
{
  "username": "admin",
  "password": "admin"
}
`
- returns a `200 OK` if the username and password is valid
- returns a `400` if the body is empty
- returns a `401` if credentials are invalid

# Analytic
## Prerequisites

- Python
- MySQL Server and pymysql Python package
- MongoDB Server and pymongo Python package

## Usage

The application will start and periodically calculate min, and max averages, then stores in MongoDB.


# Enter Data
## Prerequisites

- Python 3.x
- Flask
- SQLAlchemy
- Requests
- MySQL Server and a compatible MySQL client

## Usage
The application will start and listen on http://0.0.0.0:5000. 


# Show Results
## Prerequisites

- Python 3.x
- Flask
- pymongo
- MongoDB Server

## Usage
The application will start and listen on http://0.0.0.0:5004, navigating to the page will allow you to log in and see the data.