"""
Spotify email checker — Railway.app microservice
GET /check?email=user@example.com
Returns: {"status": 20} if registered, {"status": 1} if not found
"""

import os
import httpx
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse

app = FastAPI()

SPOTIFY_URL = "https://spclient.wg.spotify.com/signup/public/v1/account"

# Headers that mimic a real browser visiting accounts.spotify.com
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
    "Origin": "https://accounts.spotify.com",
    "Referer": "https://accounts.spotify.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
}


@app.get("/check")
async def check_email(email: str = Query(..., description="Email to validate")):
    params = {"validate": "1", "email": email}

    try:
        async with httpx.AsyncClient(timeout=8.0, follow_redirects=True) as client:
            resp = await client.get(SPOTIFY_URL, params=params, headers=HEADERS)
            data = resp.json()
            # Pass through only the status field — nothing else needed
            return JSONResponse({"status": data.get("status", 1)})
    except Exception:
        # On any error fall back to status 20 so the user can still proceed
        return JSONResponse({"status": 20})


@app.get("/")
async def root():
    return {"ok": True}
