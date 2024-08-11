import uvicorn

from pydantic import BaseModel
from fastapi import FastAPI 
from backend import get_AI_trip_plan

app = FastAPI()

class Trip_Data(BaseModel):
    destination: str
    start_date: str
    end_date: str
    activities: list[str]
    person_status: str
    budget: str
    
@app.post("/get_trip_plan/")
def get_trip_plan(trip_data: Trip_Data):
    return get_AI_trip_plan(trip_data.model_dump())


if __name__ == "__main__":
    uvicorn.run("backend_api:app", host="127.0.0.1", port=8000, reload=True)