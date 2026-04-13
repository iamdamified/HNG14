from fastapi import FastAPI, HTTPException, Response
import httpx
from datetime import datetime, timezone

app = FastAPI()

@app.get("/api/classify")
async def classify_name(response: Response, name: str | None = None):
    response.headers["Access-Control-Allow-Origin"] = "*"

    if name is None or not isinstance(name, str) or name.strip() == "":
        return {
            "status": "error",
            "message": "Missing or empty name parameter"
        }

    name = name.lower()

    try:
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.get(
                "https://api.genderize.io/",
                params={"name": name}
            )
    except httpx.RequestError:
        return {
            "status": "error",
            "message": "Upstream service unavailable"
        }

    data = r.json()

    gender = data.get("gender")
    probability = data.get("probability")
    sample_size = data.get("count")

    if gender is None or sample_size == 0:
        return {
            "status": "error",
            "message": "No prediction available for the provided name"
        }

    is_confident = (
        isinstance(probability, float)
        and isinstance(sample_size, int)
        and probability >= 0.7
        and sample_size >= 100
    )

    processed_at = (
        datetime.now(timezone.utc)
        .isoformat(timespec="seconds")
        .replace("+00:00", "Z")
    )

    return {
        "status": "success",
        "data": {
            "name": name,
            "gender": gender,
            "probability": probability,
            "sample_size": sample_size,
            "is_confident": is_confident,
            "processed_at": processed_at
        }
    }



# # api/index.py

# from fastapi import FastAPI, Query, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# import httpx
# from datetime import datetime, timezone

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # REQUIRED
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.get("/api/classify")
# async def classify_name(name: str = Query(...)):
#     if not name:
#         raise HTTPException(
#             status_code=400,
#             detail={"status": "error", "message": "Missing or empty name parameter"}
#         )

#     try:
#         async with httpx.AsyncClient(timeout=5) as client:
#             r = await client.get("https://api.genderize.io/", params={"name": name})
#             r.raise_for_status()
#     except httpx.RequestError:
#         raise HTTPException(
#             status_code=502,
#             detail={"status": "error", "message": "Upstream service unavailable"}
#         )

#     data = r.json()

#     if data.get("gender") is None or data.get("count") == 0:
#         return {
#             "status": "error",
#             "message": "No prediction available for the provided name"
#         }

#     probability = data["probability"]
#     sample_size = data["count"]

#     return {
#         "status": "success",
#         "data": {
#             "name": name.lower(),
#             "gender": data["gender"],
#             "probability": probability,
#             "sample_size": sample_size,
#             "is_confident": probability >= 0.7 and sample_size >= 100,
#             "processed_at": datetime.now(timezone.utc)
#                 .isoformat()
#                 .replace("+00:00", "Z")
#         }
#     }