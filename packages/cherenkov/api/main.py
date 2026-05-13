"""
cherenkov REST API Server
FastAPI-based API for remote workflow execution
"""

import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# sys.path manipulation removed — package is installed via pyproject.toml

from cherenkov.orchestration.orchestration_api import orchestrate_workflow
from cherenkov.orchestration.result_persistence import ResultStore
from cherenkov.orchestration.workflow_parser import load_workflow

app = FastAPI(
    title="cherenkov Autonomous Agent API",
    description="REST API for workflow orchestration and security testing",
    version="1.0.0",
)

_ALLOWED_ORIGINS = os.getenv(
    "cherenkov_CORS_ORIGINS", "http://localhost:5000,http://127.0.0.1:5000"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=_ALLOWED_ORIGINS,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)


# Models
class WorkflowExecuteRequest(BaseModel):
    workflow_name: str
    config: Optional[Dict[str, Any]] = None


class WorkflowResponse(BaseModel):
    success: bool
    workflow: str
    outputs: Dict[str, Any]
    duration: float


# Routes
@app.get("/")
async def root() -> dict:
    return {
        "message": "cherenkov Autonomous Agent API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "workflows": "/workflows",
            "execute": "/workflows/execute",
            "results": "/results",
        },
    }


@app.get("/health")
async def health() -> dict:
    return {"status": "healthy", "agents": "operational"}


@app.post("/workflows/execute", response_model=WorkflowResponse)
async def execute_workflow(request: WorkflowExecuteRequest) -> WorkflowResponse:
    """Execute a workflow by name or config"""
    try:
        # Load workflow config
        if request.config:
            config = request.config
        else:
            # Sanitize workflow_name before path construction (prevent path traversal)
            safe_name = Path(request.workflow_name).name
            if not re.fullmatch(r"[a-zA-Z0-9_-]+", safe_name):
                raise HTTPException(
                    status_code=400,
                    detail="workflow_name must contain only letters, digits, hyphens, or underscores",
                )
            workflow_path = str(Path("examples/workflows") / f"{safe_name}.yaml")
            config = load_workflow(workflow_path)

        # Execute
        result = orchestrate_workflow(config)

        # Save result
        store = ResultStore()
        store.save_result(request.workflow_name, result.outputs)

        return WorkflowResponse(
            success=result.success,
            workflow=request.workflow_name,
            outputs=result.outputs,
            duration=result.duration,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/workflows")
async def list_workflows() -> dict:
    """List available workflows"""
    from pathlib import Path

    workflows_dir = Path("examples/workflows")
    if workflows_dir.exists():
        workflows = [f.stem for f in workflows_dir.glob("*.yaml")]
        return {"workflows": workflows, "count": len(workflows)}
    return {"workflows": [], "count": 0}


@app.get("/results/{workflow_name}")
async def get_results(workflow_name: str) -> dict:
    """Get latest results for a workflow"""
    store = ResultStore()
    result = store.get_latest(workflow_name)
    if result:
        return result
    raise HTTPException(status_code=404, detail="No results found")


if __name__ == "__main__":
    import uvicorn

    host = os.getenv("cherenkov_API_HOST", "127.0.0.1")
    port = int(os.getenv("cherenkov_API_PORT", "8000"))
    uvicorn.run(app, host=host, port=port)
