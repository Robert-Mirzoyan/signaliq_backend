# SignalIQ Backend Prototype

This project is a simple backend prototype for our SignalIQ system.  
It analyzes financial transcripts or uploaded documents and produces a **Financial Signal Score (0–100)** based on sentiment and detected risk words.

The system is implemented using **Python, FastAPI, and SQLite**.

## Requirements

- Python 3.9+
- pip

## Setup

Clone the repository and install dependencies.

git clone <repo_url>  
cd signaliq_backend

Create a virtual environment:

python3 -m venv .venv  
source .venv/bin/activate

Install dependencies:

pip install -r requirements.txt

## Run the server

Start the FastAPI application:

uvicorn app.main:app --reload

The server will start at:

http://127.0.0.1:8000

## Test the API

Open the automatic API documentation in the browser:

http://127.0.0.1:8000/docs

From there you can test the endpoints.

Main endpoint:

POST /analyze/file

Upload a `.pdf` or `.txt` financial report and the system will return:

- sentiment score  
- detected risk keywords  
- final **Financial Signal Score**

## Example output

The API returns a JSON result containing sentiment, risk detection, and the final signal score.