**DOCKER COMPOSER TIER 3**

Description


This project demonstrates a classic three-tier architecture using Docker containers. It consists of a frontend Nginx reverse proxy, a backend Flask API, a PostgreSQL database, and a Redis cache. Each component runs in its own container, communicating over a Docker network defined in docker-compose.yml.

Features

    - Modular containerized architecture for easy deployment and scaling.

    - Backend API built with Flask connecting to PostgreSQL and Redis.
    
    - PostgreSQL container with persistent storage and initialization script.

    - Redis container for caching.

    - Nginx frontend acting as a reverse proxy forwarding requests to the backend API.


**Project Structure and File Breakdown**

Backend Folder (backend/)

    - app.py: Flask application implementing API endpoints to test connectivity with PostgreSQL and Redis.

    - Dockerfile: Multi-stage Dockerfile that builds and runs the Flask app with dependencies.

    - requirements.txt: Python dependencies including Flask, psycopg2-binary, and redis client.


Database Folder (database/)


    - init.sql: SQL script to create a sample table and insert initial data. This script runs automatically when the PostgreSQL container initializes.


Frontend Folder (frontend/)

    - Dockerfile: Builds an Nginx container using the alpine image.

    - nginx.conf: Nginx configuration file that sets up a reverse proxy forwarding all HTTP traffic to the backend Flask API container.


Root Files

    - .env: Environment variables for PostgreSQL credentials and hostnames, used by Docker Compose and containers.

    - docker-compose.yml: Defines four services (frontend, backend, database, redis), their build contexts or images, environment variables, ports, volumes, and dependencies.


**Containers and Their Relationships**

This project runs four containers:

    - database: Runs PostgreSQL 15 with persistent volume storage. It initializes the database using init.sql.

    - redis: Runs Redis cache server.

    - backend: Runs the Flask API. It connects to the database container for PostgreSQL and redis container for caching. It exposes port 5000.

    - frontend: Runs Nginx reverse proxy. It listens on port 80 and forwards all incoming HTTP requests to the backend API container.


The containers communicate over the default Docker network created by Docker Compose. The backend uses service names (database, redis) as hostnames to connect to the respective containers.


**HOW TO RUN THE PROJECT**

1- Clone the repository (if applicable) or ensure all files are in place with the structure described.

2- Create a .env file in the root directory with the following content:


POSTGRES_USER=admin

POSTGRES_PASSWORD=secret

POSTGRES_DB=appdb

POSTGRES_HOST=database

REDIS_HOST=redis


3- Build and start the containers using Docker Compose:


        docker-compose up --build


4- Access the frontend by navigating to http://localhost in your browser. Nginx will proxy requests to the backend API.

5- Test backend API endpoints directly (optional):


http://localhost:5000/ - Basic health check.


http://localhost:5000/db - Tests connection to PostgreSQL and returns current DB time.


http://localhost:5000/cache - Tests Redis cache functionality.


6- Stop the project by pressing Ctrl+C and optionally remove containers and volumes:


        docker-compose down -v


**Technical Skills Demonstrated**


    - Docker multi-stage builds for efficient container images.

    - Docker Compose orchestration for multi-container applications.

    - Container networking using service names for inter-container communication.

    - Flask API development with database and cache integration.

    - PostgreSQL initialization with custom SQL scripts.

    - Nginx reverse proxy configuration for routing traffic.

    - Environment variable management with .env files.

    - Persistent data storage using Docker volumes.

    - Basic caching strategies using Redis.

----------------------------------------------------------------------------------------------------------------------------------------------------------

**Next**: Pushing to ACR --> Deploying to App Service

**"PUSHING" DOCKER IMAGES TO AZURE CONTAINER REGISTRY (ACR) AND "DEPLOYING" TO AZURE APP SERVICE**

This guide explains how to push your backend and frontend Docker images to Azure Container Registry (ACR) and deploy them to Azure App Service. It also clarifies the role of each image. 

The project uses four Docker images:

    - Backend: Custom image you built and customized.

    - Frontend: Custom image you built and customized.

    - Database: Official Postgres image (postgres:15).

    - Cache: Official Redis image (redis:alpine).


**Step 1: Set Up Azure Container Registry (ACR)**

Create an Azure Container Registry in your Azure portal or via CLI.

Log in to ACR from your local machine:

    az acr login --name <your-acr-name>

**Step 2: Tag and Push Your Images to ACR**

For each custom image (backend and frontend), tag it with your ACR login server and push:

- Tag backend image

        docker tag backend <your-acr-name>.azurecr.io/backend:latest

- Push backend image
  
        docker push <your-acr-name>.azurecr.io/backend:latest

- Tag frontend image
  
        docker tag frontend <your-acr-name>.azurecr.io/frontend:latest

- Push frontend image
  
        docker push <your-acr-name>.azurecr.io/frontend:latest

**Step 3: Deploy to Azure App Service**

Here are detailed Azure CLI commands to deploy your backend and frontend images:

1- Create a resource group (if you don't have one already):
  
    az group create --name myResourceGroup --location eastus
  
2- Create an App Service plan:

    az appservice plan create --name myAppServicePlan --resource-group myResourceGroup --sku B1 --is-linux

3- Create the Web Apps for backend and frontend:

    az webapp create --resource-group myResourceGroup --plan myAppServicePlan --name myBackendApp --deployment-container-image-name <your-acr-name>.azurecr.io/backend:latest

    az webapp create --resource-group myResourceGroup --plan myAppServicePlan --name myFrontendApp --deployment-container-image-name <your-acr-name>.azurecr.io/frontend:latest

4- Configure the Web Apps to use your Azure Container Registry:

    az webapp config container set --name myBackendApp --resource-group myResourceGroup --docker-custom-image-name <your-acr-name>.azurecr.io/backend:latest --docker-registry-server-url https://<your-acr-name>.azurecr.io

    az webapp config container set --name myFrontendApp --resource-group myResourceGroup --docker-custom-image-name <your-acr-name>.azurecr.io/frontend:latest --docker-registry-server-url https://<your-acr-name>.azurecr.io

5- Set environment variables (e.g., database connection string) for backend app:

    az webapp config appsettings set --resource-group myResourceGroup --name myBackendApp --settings DATABASE_URL="postgres://user:password@your-db-host:5432/dbname"

6- Restart the Web Apps to apply changes:

    az webapp restart --name myBackendApp --resource-group myResourceGroup
    az webapp restart --name myFrontendApp --resource-group myResourceGroup

7- Verify deployment by browsing to the URLs:

    https://myBackendApp.azurewebsites.net
    https://myFrontendApp.azurewebsites.net
