# flight_search_api.py

from fastapi import FastAPI, Query
from flight_search_automation import search_flights

app = FastAPI(title="Flight Search API")

@app.get("/flight-search")
def flight_search(
    origin: str = Query("Bangalore"),
    destination: str = Query("Delhi"),
    journey_date: str = Query(None)
):
    """
    Example:
    GET /flight-search?origin=Bangalore&destination=Delhi&journey_date=2025-10-18
    """
    results = search_flights(origin, destination, journey_date)
    return results
