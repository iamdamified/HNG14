# Gender Classification API

A simple, production-ready REST API that classifies a given name by gender using the Genderize API, applies confidence logic, and returns a clean, structured response.

This project was built for the **API Integration & Data Processing Assessment (Stage 0)**.

---

##  Live API Endpoint

```
GET https://hng14gendername.vercel.app/api/classify?name={name}
```

### Example
```
GET https://hng14gendername.vercel.app/api/classify?name=emmanuel
```

---

##  What This API Does

- Accepts a `name` query parameter
- Calls an external gender prediction API
- Renames and restructures third-party data
- Applies confidence rules
- Handles edge cases and errors gracefully
- Returns consistent JSON responses
- Includes required CORS headers

---

##  Tech Stack

- Python
- FastAPI
- httpx (async HTTP client)
- Vercel (serverless deployment)

---

##  API Specification

### Endpoint
```
GET /api/classify?name={name}
```

---

###  Success Response (200 OK)

```json
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
```

---

##  Processing Rules

- `count` from the external API is renamed to `sample_size`
- `is_confident` is **true only if**:
  - `probability ≥ 0.7`
  - `sample_size ≥ 100`
- `processed_at` is generated dynamically on every request
  - UTC
  - ISO-8601 format
  - Not hardcoded
- Name is normalized to lowercase

---

##  Error Handling

All error responses follow this structure:

```json
{
  "status": "error",
  "message": "<error message>"
}
```

### Supported Error Scenarios

| Scenario | HTTP Status | Message |
|--------|------------|---------|
| Missing or empty name | 400 | Missing or empty name parameter |
| Invalid name type | 422 | Name must be a string |
| No prediction available | 200 | No prediction available for the provided name |
| External API failure | 502 | Upstream service unavailable |

---

##  Edge Case Handling

If the external API returns:
- `gender: null`, or
- `count: 0`

The API responds with:

```json
{
  "status": "error",
  "message": "No prediction available for the provided name"
}
```

---

##  CORS Configuration

The API includes the required header:

```
Access-Control-Allow-Origin: *
```

This allows unrestricted access by grading scripts and external clients.

---

##  Running Locally

### 1. Clone the repository
```
git clone https://github.com/iamdamified/HNG14.git
cd HNG14
```

### 2. Create and activate a virtual environment
```
pip install virtualenv
virtualenv genderenv
source ./genderenv/scripts/activate
```

### 3. Install dependencies
```
pip install -r requirements.txt
```

### 4. Run the application
```
uvicorn api.index:app --reload
```

API will be available at:
```
http://127.0.0.1:8000/api/classify?name=emmanuel
```

---

##  Deployment

The application is deployed on Vercel using Python serverless functions.

- No background workers
- No persistent server
- Handles multiple concurrent requests
- Response time under 500ms (excluding external API latency)

---

##  Testing

You can test using:
- Browser
- Postman
- Curl

Example:
```
curl "https://hng14gendername.vercel.app/api/classify?name=emmanuel"
```

---

## API documentation
Postman : "https://documenter.getpostman.com/view/27321084/2sBXitCnNL"

---

##  Submission Checklist

-  Single GET endpoint
-  External API integration
-  Data extraction and renaming
-  Confidence logic implemented
-  Edge cases handled
-  CORS enabled
-  Error format standardized
-  README included
-  Live deployed endpoint tested

---

##  License

This project is provided for assessment and evaluation purposes.

---

###  Final Note

This API strictly follows all assessment requirements and is ready for automated grading and manual review.

