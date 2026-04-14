from fastapi import FastAPI, Query, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
import httpx
from datetime import datetime, timezone

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GENDERIZE_URL = "https://api.genderize.io"

@app.get("")
async def classify_name(
    response: Response,
    name: str | None = Query(default=None)
):
    response.headers["Access-Control-Allow-Origin"] = "*"

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

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            r = await client.get(GENDERIZE_URL, params={"name": name})
            r.raise_for_status()
    except httpx.RequestError:
        raise HTTPException(
            status_code=502,
            detail={"status": "error", "message": "Upstream service unavailable"}
        )

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
        isinstance(probability, (int, float))
        and probability >= 0.7
        and sample_size >= 100
    )

    processed_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

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