import os
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from decision_engine import DecisionIntelligenceEngine
from data_generator import generate_kpi_dataset

app = FastAPI(title="Executive Decision Intelligence System")

if not os.path.exists("executive_kpis.json"):
    generate_kpi_dataset()

engine = DecisionIntelligenceEngine()

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/api/kpis")
async def get_kpis():
    return engine.analyze()

@app.post("/api/recalculate")
async def recalculate():
    generate_kpi_dataset()
    global engine
    engine = DecisionIntelligenceEngine()
    return {"status": "success", "message": "Re-simulated executive metrics."}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8008, reload=True)
