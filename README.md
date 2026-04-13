# Gender Classification API

A production-ready REST API that classifies a given name by gender using the Genderize API, applies strict confidence logic, and returns a clean, structured response.

This project was built for the **API Integration & Data Processing Assessment (Stage 0)** and is fully compliant with all grading requirements.

---

## Live API Endpoint

```
GET https://hng14gendername.vercel.app/api/classify?name={name}
```

### Example Request
```
GET https://hng14gendername.vercel.app/api/classify?name=emmanuel
```

---

## What This API Does

- Accepts a `name` query parameter
- Integrates with the external **Genderize API**
- Extracts and restructures third-party data
- Renames fields according to specification
- Applies strict confidence rules
- Handles validation errors and edge cases
- Returns consistent JSON responses
- Includes required CORS headers for public access

---

## Tech Stack

- Python
- FastAPI
- httpx (asynchronous HTTP client)
- Vercel (serverless deployment)

---

## API Specification

### Endpoint
```
GET /api/classify?name={name}
```

---

### Success Response (200 OK)

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

## Processing Rules

- `count` from the external API is renamed to `sample_size`
- `is_confident` is **true only if**:
  - `probability ≥ 0.7`, **and**
  - `sample_size ≥ 100`
- `processed_at` is generated dynamically on every request
  - UTC timezone
  - ISO 8601 format
  - Never hardcoded
- Input name is normalized to lowercase

---

## Error Handling

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
| Missing name parameter | 400 | Missing name parameter |
| Empty name parameter | 400 | Empty name parameter |
| Invalid name type | 422 | Name must be a string |
| No prediction available | 200 | No prediction available for the provided name |
| External API failure | 502 | Upstream service unavailable |

---

## Edge Case Handling

If the external API returns:
- `gender: null`, **or**
- `count: 0`

The API responds with:

```json
{
  "status": "error",
  "message": "No prediction available for the provided name"
}
```

---

## CORS Configuration

The API explicitly includes the required header:

```
Access-Control-Allow-Origin: *
```

This ensures unrestricted access by grading scripts and external clients.

---

## Running Locally

### 1. Clone the repository
```
git clone https://github.com/iamdamified/HNG14.git
cd HNG14
```

### 2. Create and activate a virtual environment
```
python -m venv venv
source venv/Scripts/activate   # Windows
source venv/bin/activate       # macOS/Linux
```

### 3. Install dependencies
```
pip install -r requirements.txt
```

### 4. Run the application
```
uvicorn main:app --reload
```

The API will be available at:
```
http://127.0.0.1:8000/api/classify?name=emmanuel
```

---

## Deployment

The application is deployed on **Vercel** using Python serverless functions.

- No background workers
- No persistent server
- Handles multiple concurrent requests
- Optimized for fast cold starts
- Meets response-time requirements (excluding external API latency)
- the path is "api" folder, and "index.py" file

---

## Testing

You can test the API using:
- Browser
- Postman
- cURL

Example:
```
curl "https://hng14gendername.vercel.app/api/classify?name=emmanuel"
```

---

## API Documentation

Postman Documentation:
```
https://documenter.getpostman.com/view/27321084/2sBXitCnNL
```

---

## Submission Checklist

-  Single GET endpoint
-  External API integration
-  Correct data extraction and renaming
-  Confidence logic implemented
-  Edge cases handled
-  CORS enabled
-  Error format standardized
-  README included
-  Live deployed endpoint tested

---

## License

This project is provided strictly for assessment and evaluation purposes.

---

###  Final Note

This API strictly follows all Stage 0 assessment requirements and is fully ready for automated grading and manual review.

