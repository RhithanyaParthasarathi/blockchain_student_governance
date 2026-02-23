# Student Governance System - Backend API

This directory contains the backend implementation for Developer 2. It integrates with a local MongoDB database to manage student identities securely and serves as a bridge to the private blockchain network.

## Technology Stack
- **FastAPI**: High-performance web framework.
- **MongoDB (Motor)**: Async database driver for storing student credentials and eligibility.
- **JWT (python-jose & passlib)**: Secure authentication and authorization.
- **HTTPX**: Async HTTP client to communicate with the blockchain nodes.

## Prerequisites
- **Python 3.8+**
- **MongoDB** instance running locally (`mongodb://localhost:27017`) or configure `MONGO_URL` env variable.
- The **Blockchain Nodes** must be running (e.g. via `../blockchain_model/start_nodes.sh`).

## Setup & Running
1. Open a terminal and install dependencies from the root directory:
   ```bash
   pip install -r requirements.txt
   ```
2. Change into the backend directory and start the server:
   ```bash
   cd backend
   uvicorn main:app --reload --port 8000
   ```
3. Open the interactive API docs at:
   [http://localhost:8000/docs](http://localhost:8000/docs)

## API Flow
1. **`POST /register`**: Register a new student profile.
2. **`POST /login`**: Authenticate and receive a JWT access token.
3. **`GET /elections`**: Retrieve the current list of candidates.
4. **`POST /vote`**: Submit a vote securely. The backend will verify your token, check your `has_voted` status in MongoDB, relay the vote to the blockchain node (port 5000), trigger block mining, and finally update your state in MongoDB.
5. **`GET /results`**: Fetches the entire blockchain history and computes the exact voting results on-the-fly.
