from fastapi import FastAPI, Query, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
import httpx
from datetime import datetime, timezone

app = FastAPI()

# --------------------
# CORS CONFIGURATION
# --------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # REQUIRED
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GENDERIZE_URL = "https://api.genderize.io"

@app.get("/api/classify")
async def classify_name(
    response: Response,
    name: str | None = Query(default=None)
):
    # Ensure CORS header ALWAYS exists
    response.headers["Access-Control-Allow-Origin"] = "*"

    # --------------------
    # VALIDATION
    # --------------------
    if name is None:
        raise HTTPException(
            status_code=400,
            detail={"status": "error", "message": "Missing name parameter"}
        )

    if not isinstance(name, str):
        raise HTTPException(
            status_code=422,
            detail={"status": "error", "message": "Name must be a string"}
        )

    name = name.strip()
    if name == "":
        raise HTTPException(
            status_code=400,
            detail={"status": "error", "message": "Empty name parameter"}
        )

    # --------------------
    # EXTERNAL API CALL
    # --------------------
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            api_response = await client.get(
                GENDERIZE_URL,
                params={"name": name}
            )
            api_response.raise_for_status()
    except httpx.RequestError:
        raise HTTPException(
            status_code=502,
            detail={"status": "error", "message": "Upstream service unavailable"}
        )

    data = api_response.json()

    gender = data.get("gender")
    probability = data.get("probability")
    sample_size = data.get("count")

    # --------------------
    # EDGE CASE HANDLING
    # --------------------
    if gender is None or sample_size == 0:
        raise HTTPException(
            status_code=200,
            detail={
                "status": "error",
                "message": "No prediction available for the provided name"
            }
        )

    # --------------------
    # CONFIDENCE LOGIC
    # --------------------
    is_confident = (
        isinstance(probability, (int, float))
        and probability >= 0.7
        and sample_size >= 100
    )

    # --------------------
    # TIMESTAMP
    # --------------------
    processed_at = (
        datetime.now(timezone.utc)
        .isoformat()
        .replace("+00:00", "Z")
    )

    # --------------------
    # SUCCESS RESPONSE
    # --------------------
    return {
        "status": "success",
        "data": {
            "name": name.lower(),
            "gender": gender,
            "probability": probability,
            "sample_size": sample_size,
            "is_confident": is_confident,
            "processed_at": processed_at
        }
    }

# Run locally with:
# uvicorn main:app --reload





# from fastapi import FastAPI, Query, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# import httpx
# from datetime import datetime, timezone

# app = FastAPI()

# # --------------------
# # CORS CONFIGURATION
# # --------------------
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # REQUIRED BY TASK
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# GENDERIZE_URL = "https://api.genderize.io/"

# @app.get("/api/classify")
# async def classify_name(name: str = Query(...)):

#     # VALIDATION
#     if not name:
#         raise HTTPException(
#             status_code=400,
#             detail={"status": "error", "message": "Missing or empty name parameter"}
#         )

#     if not isinstance(name, str):
#         raise HTTPException(
#             status_code=422,
#             detail={"status": "error", "message": "Name must be a string"}
#         )


#     # EXTERNAL API CALL
#     try:
#         async with httpx.AsyncClient(timeout=5.0) as client:
#             response = await client.get(GENDERIZE_URL, params={"name": name})
#             response.raise_for_status()
#     except httpx.RequestError:
#         raise HTTPException(
#             status_code=502,
#             detail={"status": "error", "message": "Upstream service unavailable"}
#         )

#     data = response.json()

#     gender = data.get("gender")
#     probability = data.get("probability")
#     count = data.get("count")


#     # EDGE CASE HANDLING
#     if gender is None or count == 0:
#         raise HTTPException(
#             status_code=200,
#             detail={
#                 "status": "error",
#                 "message": "No prediction available for the provided name"
#             }
#         )

  
#     # PROCESSING LOGIC
#     sample_size = count
#     is_confident = probability >= 0.7 and sample_size >= 100

#     processed_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

   
#     # SUCCESS RESPONSE
#     return {
#         "status": "success",
#         "data": {
#             "name": name.lower(),
#             "gender": gender,
#             "probability": probability,
#             "sample_size": sample_size,
#             "is_confident": is_confident,
#             "processed_at": processed_at
#         }
#     }


# #use "uvicorn main:app --reload" to run the server in development mode
