import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, List

logger = logging.getLogger("cherenkov.mesh")


@dataclass
class MeshNode:
    id: str
    ip: str
    port: int
    status: str
    last_seen: datetime


class MeshManager:
    """Manages the distributed scan mesh. Tracks peer nodes and availability."""

    def __init__(self):
        self.nodes: Dict[str, MeshNode] = {}
        # In a real implementation, Zeroconf listeners would populate this.
        # For the Ph5 MVP, we implement the tracking logic.

    def register_node(self, node_id: str, ip: str, port: int):
        self.nodes[node_id] = MeshNode(
            id=node_id, ip=ip, port=port, status="online", last_seen=datetime.now(timezone.utc)
        )
        logger.info("Mesh node registered: %s @ %s:%d", node_id, ip, port)

    def get_active_nodes(self) -> List[MeshNode]:
        # Cleanup stale nodes (older than 60s)
        now = datetime.now(timezone.utc)
        active = []
        for node in self.nodes.values():
            if (now - node.last_seen).total_seconds() < 60:
                active.append(node)
        return active

    async def distribute_scan(self, scan_request: dict) -> dict:
        """Splits a scan across available nodes."""
        nodes = self.get_active_nodes()
        if not nodes:
            return {"status": "error", "message": "No active mesh nodes available"}

        # Simple round-robin or broadcast
        # For Ph5, we return a plan
        return {
            "status": "distributed",
            "nodes_engaged": [n.id for n in nodes],
            "plan": f"Scan split into {len(nodes)} chunks",
        }


# Global instance for the API
mesh_manager = MeshManager()
