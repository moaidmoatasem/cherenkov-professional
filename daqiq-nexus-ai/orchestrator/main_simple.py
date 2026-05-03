from datetime import datetime
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="DAQIQ Orchestrator - Simplified")


class ScanRequest(BaseModel):
    target: str
    scan_types: List[str] = ["ai-agent"]


@app.get("/")
async def root():
    return {"service": "DAQIQ NEXUS Orchestrator", "version": "1.0.0", "status": "running"}


@app.post("/api/scan")
async def start_scan(request: ScanRequest):
    scan_id = f"scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    # Simulate scan without Redis
    return {
        "scan_id": scan_id,
        "status": "completed",
        "target": request.target,
        "results": {
            "vulnerabilities": [
                {
                    "type": "SQL Injection",
                    "severity": "HIGH",
                    "description": "Potential SQL injection found",
                    "source_scanner": "AI Agent",
                },
                {
                    "type": "XSS",
                    "severity": "MEDIUM",
                    "description": "Cross-site scripting vulnerability",
                    "source_scanner": "AI Agent",
                },
            ],
            "summary": {"critical": 0, "high": 1, "medium": 1, "low": 0, "total": 2},
        },
    }


if __name__ == "__main__":
    import uvicorn

    print("🚀 Starting simplified DAQIQ Orchestrator...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
