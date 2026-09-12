import os

import requests
from dotenv import load_dotenv


load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST")

LIVE_MATCHES_URL = (
    "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live"
)

SCORECARD_URL = (
    "https://cricbuzz-cricket.p.rapidapi.com/mcenter/v1/{match_id}/scard"
)


def get_live_matches():
    """Fetch live matches from Cricbuzz RapidAPI."""

    if not RAPIDAPI_KEY or not RAPIDAPI_HOST:
        raise ValueError("RapidAPI credentials are missing.")

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST,
    }

    response = requests.get(
        LIVE_MATCHES_URL,
        headers=headers,
        timeout=15,
    )

    response.raise_for_status()

    return response.json()

def get_scorecard(match_id):
    """Fetch scorecard data for a specific match."""

    if not RAPIDAPI_KEY or not RAPIDAPI_HOST:
        raise ValueError("RapidAPI credentials are missing.")

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST,
    }

    url = SCORECARD_URL.format(match_id=match_id)

    response = requests.get(
        url,
        headers=headers,
        timeout=15,
    )

    response.raise_for_status()

    return response.json()