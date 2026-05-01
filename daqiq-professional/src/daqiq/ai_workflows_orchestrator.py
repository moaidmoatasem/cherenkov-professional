"""
AI Workflows Orchestrator for daqiq.

TODO:
- Define standard interface for AI agents (input, output, context)
- Add orchestration logic for autonomous roadmap execution
- Implement logging & metrics hooks for long-running workflows
"""

from typing import Callable, Dict, Any, List
from daqiq.ai_workflows_orchestrator import orchestrate_ai_workflows

def echo_agent(payload):
    return {"echo": payload}

context = {
    "project_name": "Demo AI Orchestration",
    "roadmap": [
        {"name": "Echo Hello", "agent": "echo", "input": {"message": "hello"}},
        {"name": "No agent step"},
    ],
    "agents": {
        "echo": echo_agent,
    },
}

orchestrate_ai_workflows(context)

AgentFn = Callable[[Dict[str, Any]], Dict[str, Any]]


class AgentRegistry:
    """
    Minimal in-memory registry for AI agents participating in workflows.
    """

    def __init__(self) -> None:
        self._agents: Dict[str, AgentFn] = {}

    def register(self, name: str, agent_fn: AgentFn) -> None:
        if name in self._agents:
            raise ValueError(f"Agent '{name}' is already registered")
        self._agents[name] = agent_fn

    def get(self, name: str) -> AgentFn:
        try:
            return self._agents[name]
        except KeyError as exc:
            raise ValueError(f"Agent '{name}' is not registered") from exc

    def list_agents(self) -> List[str]:
        return list(self._agents.keys())


def orchestrate_ai_workflows(context: Dict[str, Any]) -> None:
    """
    Entry point for AI workflows orchestration.

    :param context: High-level configuration and runtime context for agents.
                    Expected keys:
                      - project_name: str
                      - roadmap: list[dict] (high-level tasks/steps)
                      - agents: dict[str, AgentFn] or similar
    """
    # 1. Validate context
    required_keys = ["project_name", "roadmap", "agents"]
    missing = [k for k in required_keys if k not in context]
    if missing:
        raise ValueError(f"Missing required context keys: {missing}")

    project_name = context["project_name"]
    roadmap = context["roadmap"]
    agents_mapping = context["agents"]

    if not isinstance(roadmap, list):
        raise ValueError("context['roadmap'] must be a list of steps")

    if not isinstance(agents_mapping, dict):
        raise ValueError("context['agents'] must be a dict of agent callables")

    registry = AgentRegistry()

    # 2. Register agents from context
    for name, fn in agents_mapping.items():
        if not callable(fn):
            raise ValueError(f"Agent '{name}' is not callable")
        registry.register(name, fn)

    # 3. Simple run loop stub over roadmap steps
    print(f"[daqiq-ai] Starting orchestration for project: {project_name}")
    for idx, step in enumerate(roadmap, start=1):
        step_name = step.get("name", f"step-{idx}")
        agent_name = step.get("agent")
        print(f"[daqiq-ai] Executing step {idx}: {step_name} using agent '{agent_name}'")

        if not agent_name:
            print(f"[daqiq-ai] Skipping step {idx}: no agent specified")
            continue

        try:
            agent_fn = registry.get(agent_name)
        except ValueError as exc:
            print(f"[daqiq-ai] Error: {exc}")
            continue

        # In a real implementation we would pass richer context and handle outputs.
        agent_input = step.get("input", {})
        try:
            result = agent_fn(agent_input)
            print(f"[daqiq-ai] Step {idx} completed with result: {result}")
        except Exception as exc:  # noqa: BLE001
            print(f"[daqiq-ai] Step {idx} failed with error: {exc}")

    print(f"[daqiq-ai] Orchestration finished for project: {project_name}")