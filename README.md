Gender Classification API

A lightweight REST API that classifies a given name by gender using the Genderize API, applies confidence logic, and returns a processed, structured response.

This project was built as part of an API Integration & Data Processing Assessment.

🚀 Live Endpoint
GET /api/classify?name={name}
📌 Features
Integrates with an external gender prediction API
Renames and restructures third-party data
Applies confidence rules to predictions
Handles edge cases and validation errors
Returns consistent, structured JSON responses
Includes required CORS headers for public access
Designed for high availability and fast response time
🛠 Tech Stack
Python
FastAPI
httpx (async HTTP client)
Uvicorn (ASGI server)
📥 Installation & Setup
1. Clone the repository
git clone https://github.com/your-username/gender-classifier-api.git
cd gender-classifier-api
2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate     # Windows: venv\Scripts\activate
3. Install dependencies
pip install -r requirements.txt
▶️ Running the Application

Start the server locally:

uvicorn main:app --reload

The API will be available at:

http://127.0.0.1:8000
📡 API Usage
Classify Name
GET /api/classify?name=john
Successful Response (200 OK)
{
  "status": "success",
  "data": {
    "name": "john",
    "gender": "male",
    "probability": 0.99,
    "sample_size": 1234,
    "is_confident": true,
    "processed_at": "2026-04-01T12:00:00Z"
  }
}
⚙️ Processing Rules
count from the external API is renamed to sample_size
is_confident is true only if:
probability ≥ 0.7
sample_size ≥ 100
processed_at is generated dynamically in UTC ISO-8601 format
Name is normalized to lowercase
❗ Error Handling

All error responses follow this format:

{
  "status": "error",
  "message": "<error message>"
}
Supported Error Cases
Scenario	HTTP Status	Message
Missing or empty name	400	Missing or empty name parameter
Name is not a string	422	Name must be a string
Gender prediction unavailable	200	No prediction available for the provided name
External API failure	502	Upstream service unavailable
🧠 Edge Case Handling

If the external API returns:

gender: null
or count: 0

The API responds with:

{
  "status": "error",
  "message": "No prediction available for the provided name"
}
🌍 CORS Configuration

The API includes the required header:

Access-Control-Allow-Origin: *

This allows the grading system and external clients to access the endpoint.

🚢 Deployment

The application can be deployed on any of the following platforms:

Vercel
Railway
Heroku
AWS
PXXL App

⚠️ Render is not supported as per assessment instructions.

🧪 Testing

You can test the API using:

Browser
Postman
Curl

Example:

curl "http://127.0.0.1:8000/api/classify?name=mark"
📄 License

This project is provided for assessment and evaluation purposes.