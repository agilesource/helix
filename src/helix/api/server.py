"""
Helix REST API Server

FastAPI-based REST API for Helix:
- Skill execution
- Plugin management
- Status monitoring
- Webhook handlers
"""

import asyncio
from contextlib import asynccontextmanager
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


# Request/Response Models

class SkillRequest(BaseModel):
    """Skill execution request"""
    skill: str
    parameters: Dict[str, Any] = {}
    context: Optional[Dict[str, Any]] = None


class SkillResponse(BaseModel):
    """Skill execution response"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    execution_time_ms: Optional[int] = None
    errors: Optional[List[str]] = None


class PluginInfo(BaseModel):
    """Plugin information"""
    name: str
    version: str
    type: str
    status: str
    description: str


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    uptime_seconds: float
    active_engines: int
    loaded_plugins: int


# Global state
from typing import Any
_app_state: dict[str, Any] = {
    "start_time": None,
    "version": "0.8.0",
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan"""
    import time
    _app_state["start_time"] = time.time()
    yield
    # Cleanup


# Create FastAPI app
app = FastAPI(
    title="Helix API",
    description="AI Era Software Engineering Methodology - REST API",
    version="0.8.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    import time
    from helix.engines import get_engine_manager

    manager = get_engine_manager()
    status_data = manager.get_status()

    return HealthResponse(
        status="healthy",
        version=str(_app_state["version"]),
        uptime_seconds=time.time() - float(_app_state["start_time"] or 0),
        active_engines=len(status_data.get("engines", {})),
        loaded_plugins=0,
    )


# Skills endpoints

@app.post("/api/skills/execute", response_model=SkillResponse)
async def execute_skill(request: SkillRequest):
    """Execute a skill"""
    from helix.core.intent import Intent, IntentType
    from helix.core.orchestrator import HelixOrchestrator

    # Map skill name to intent type
    skill_to_intent = {
        "spec": IntentType.SPEC,
        "build": IntentType.BUILD,
        "verify": IntentType.VERIFY,
        "ship": IntentType.SHIP,
        "review": IntentType.REVIEW,
        "test": IntentType.TEST,
        "qa": IntentType.TEST,
        "audit": IntentType.AUDIT,
        "gate": IntentType.GATE,
        "browse": IntentType.BROWSE,
        "design": IntentType.DESIGN,
        "learn": IntentType.LEARN,
        "checkpoint": IntentType.CHECKPOINT,
    }

    intent_type = skill_to_intent.get(request.skill.lower())
    if not intent_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unknown skill: {request.skill}"
        )

    # Create intent
    intent = Intent(
        type=intent_type,
        raw_input=request.skill,
        confidence=0.9,
        parameters=request.parameters
    )

    # Execute via orchestrator
    try:
        orchestrator = HelixOrchestrator()
        skill = orchestrator.resolve_skill(intent)

        if not skill:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Skill not found: {request.skill}"
            )

        result = await skill.execute(intent, None)

        return SkillResponse(
            success=result.success,
            message=result.message,
            data=result.data,
            execution_time_ms=result.execution_time_ms,
            errors=result.errors
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.get("/api/skills")
async def list_skills():
    """List all available skills"""
    from helix.skills import (
        SpecSkill, BuildSkill, VerifySkill, ReviewSkill,
        ShipSkill, QASkill, AuditSkill, GateSkill,
        BrowseSkill, DesignSkill, LearnSkill, CheckpointSkill
    )

    skills = [
        {"name": "spec", "category": "Execution", "status": "In Design"},
        {"name": "build", "category": "Execution", "status": "In Design"},
        {"name": "verify", "category": "Execution", "status": "In Design"},
        {"name": "ship", "category": "Execution", "status": "In Design"},
        {"name": "review", "category": "Quality", "status": "Stable"},
        {"name": "test", "category": "Quality", "status": "In Design"},
        {"name": "audit", "category": "Quality", "status": "In Design"},
        {"name": "gate", "category": "Quality", "status": "In Design"},
        {"name": "browse", "category": "Infrastructure", "status": "Stable"},
        {"name": "design", "category": "Infrastructure", "status": "Stable"},
        {"name": "learn", "category": "Infrastructure", "status": "Stable"},
        {"name": "checkpoint", "category": "Infrastructure", "status": "Stable"},
    ]

    return {"skills": skills, "total": len(skills)}


# Intent recognition

class IntentRequest(BaseModel):
    """Intent recognition request"""
    text: str


class IntentResponse(BaseModel):
    """Intent recognition response"""
    intent: str
    confidence: float
    source: str
    alternatives: Optional[List[Dict[str, Any]]] = None


@app.post("/api/intent/recognize", response_model=IntentResponse)
async def recognize_intent(request: IntentRequest):
    """Recognize intent from text"""
    from helix.engines import get_recognizer

    recognizer = get_recognizer()
    result = recognizer.recognize(request.text)

    return IntentResponse(
        intent=result.intent.type.value,
        confidence=result.confidence,
        source=result.source.value,
        alternatives=[
            {"intent": i.value, "confidence": c}
            for i, c in result.alternatives
        ] if result.alternatives else None
    )


# Engine management

@app.get("/api/engines")
async def list_engines():
    """List all AI engines"""
    from helix.engines import get_engine_manager

    manager = get_engine_manager()
    return manager.get_status()


# Plugin management

@app.get("/api/plugins")
async def list_plugins():
    """List all plugins"""
    return {
        "plugins": [],
        "total": 0,
        "message": "Plugin system available but no plugins loaded"
    }


# Webhook endpoints

class WebhookRequest(BaseModel):
    """Generic webhook request"""
    event: str
    data: Dict[str, Any]


@app.post("/api/webhooks/trigger")
async def trigger_webhook(request: WebhookRequest):
    """Trigger a webhook event"""
    # Handle webhook events
    handlers = {
        "git.push": _handle_git_push,
        "git.pull_request": _handle_pull_request,
        "ci.completed": _handle_ci_completed,
        "deployment.started": _handle_deployment_started,
        "deployment.completed": _handle_deployment_completed,
    }

    handler = handlers.get(request.event)
    if handler:
        return await handler(request.data)

    return {"status": "ok", "message": f"Event {request.event} received"}


async def _handle_git_push(data: Dict[str, Any]) -> Dict[str, Any]:
    """Handle git push event"""
    return {
        "status": "processed",
        "action": "Analyzing changes for review",
        "branch": data.get("ref", "").split("/")[-1]
    }


async def _handle_pull_request(data: Dict[str, Any]) -> Dict[str, Any]:
    """Handle pull request event"""
    return {
        "status": "processed",
        "action": "Running pre-merge checks",
        "pr_number": data.get("number", 0)
    }


async def _handle_ci_completed(data: Dict[str, Any]) -> Dict[str, Any]:
    """Handle CI completion event"""
    return {
        "status": "processed",
        "action": "Analyzing test results",
        "passed": data.get("passed", False)
    }


async def _handle_deployment_started(data: Dict[str, Any]) -> Dict[str, Any]:
    """Handle deployment started event"""
    return {
        "status": "processed",
        "action": "Starting canary monitoring"
    }


async def _handle_deployment_completed(data: Dict[str, Any]) -> Dict[str, Any]:
    """Handle deployment completed event"""
    return {
        "status": "processed",
        "action": "Verifying deployment health"
    }


# CLI helper function
def run_server(host: str = "0.0.0.0", port: int = 8080):
    """Run the API server"""
    import uvicorn
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    run_server()
