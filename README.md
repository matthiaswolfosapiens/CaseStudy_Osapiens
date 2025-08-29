# Case Study: Ticket API Service

Welcome to the Osapiens Case Study! This project is a small but complete API service for retrieving ticket data. It's built with FastAPI, uses MongoDB for persistence, and is fully containerized with Docker.

---

## Project Structure

The project is organized into several directories to separate concerns:

```
.
├── Dockerfile              # Defines the Docker image for the API
├── README.md               # This file
├── api/                    # FastAPI routers and dependencies
├── core/                   # Application configuration
├── docker-compose.yml      # Defines services for Docker Compose
├── main.py                 # Main application entry point
├── models/                 # Pydantic and Beanie data models
├── requirements.txt        # Python dependencies
├── services/               # Business logic
└── test/                   # Test scripts
```

---

## Setup & How to Run

You will need **Docker** and **Docker Compose** installed to run this project.

### Step 1: Create your Environment File

The application uses a `.env` file for configuration. Create your own by copying the example file:

```bash
cp .env.example .env
```

This file already contains the first API key you will need.

### Step 2: Build and Run the Containers

Use Docker Compose to build the images and start the API service and the MongoDB database:

```bash
docker compose up --build
```

The API will be available at `http://localhost:8000`. You can access the interactive OpenAPI documentation (Swagger UI) at `http://localhost:8000/docs`.

---

## How to Use the Existing Endpoints

You can use any API client (like `curl`, Postman, or Insomnia) to interact with the existing endpoints and test your setup.

### Endpoint V1

This is the endpoint you have access to from the start.

* **URL:** `http://localhost:8000/api/v1/tickets`
* **Method:** `GET`
* **Required Header:** `X-API-KEY`

**Example `curl` command:**
(First, get the `API_KEY_V1` value from your `.env` file)

```bash
curl -X GET "http://localhost:8000/api/v1/tickets" \
     -H "X-API-KEY: d8a3a3e6-9b0a-4b3c-8f2d-1e4a6c8b0a2d"
```

### Endpoint V2

During our follow-up interview, we will provide you with the key for this second endpoint to discuss your solution and the project.

* **URL:** `http://localhost:8000/api/v2/tickets`
* **Method:** `GET`
* **Required Header:** `X-API-KEY`

