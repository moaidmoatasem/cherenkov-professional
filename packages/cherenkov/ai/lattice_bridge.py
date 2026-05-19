import logging
import hashlib
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct

logger = logging.getLogger(__name__)

COLLECTION_NAME = "cherenkov_findings"
VECTOR_SIZE = 384
QDRANT_URL = "http://localhost:6333"

_qdrant = None
_encoder = None

def _get_qdrant():
    global _qdrant
    if _qdrant is not None:
        return _qdrant
    try:
        _qdrant = QdrantClient(url=QDRANT_URL)
        if not _qdrant.collection_exists(COLLECTION_NAME):
            _qdrant.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
            )
        return _qdrant
    except Exception as e:
        logger.warning(f"Qdrant client initialization failed: {e}")
        _qdrant = False # use False to distinguish from uninitialized None
        return None

def _get_encoder():
    global _encoder
    if _encoder is not None:
        return _encoder if _encoder is not False else None
    try:
        from sentence_transformers import SentenceTransformer
        _encoder = SentenceTransformer("all-MiniLM-L6-v2")
        return _encoder
    except Exception as e:
        logger.warning(f"SentenceTransformer initialization failed: {e}")
        _encoder = False
        return None

def _generate_id(finding_id: str) -> int:
    return int(hashlib.md5(finding_id.encode()).hexdigest(), 16) % ((1<<63)-1)

def embed_and_store(trace: dict) -> str:
    """Embeds a finding trace and stores it in Qdrant."""
    qdrant = _get_qdrant()
    encoder = _get_encoder()

    if not qdrant or not encoder:
        logger.warning("Qdrant unavailable, skipping embed_and_store.")
        return ""

    try:
        finding_id = trace.get("finding_id", "unknown")
        text = trace.get("title", "") + " " + trace.get("description", "")

        vector = encoder.encode(text).tolist()

        qdrant.upsert(
            collection_name=COLLECTION_NAME,
            points=[
                PointStruct(
                    id=_generate_id(finding_id),
                    vector=vector,
                    payload=trace
                )
            ]
        )
        return finding_id
    except Exception as e:
        logger.warning(f"Failed to store embedding: {e}")
        return ""

def query_similar_targets(target: str, limit: int = 5) -> list:
    """Queries LATTICE for similar findings based on target string."""
    qdrant = _get_qdrant()
    encoder = _get_encoder()

    if not qdrant or not encoder:
        logger.warning("Qdrant unavailable, skipping query_similar_targets.")
        return []

    try:
        vector = encoder.encode(target).tolist()
        results = qdrant.search(
            collection_name=COLLECTION_NAME,
            query_vector=vector,
            limit=limit,
        )
        return [res.payload for res in results]
    except Exception as e:
        logger.warning(f"Failed to query similar targets: {e}")
        return []

def label_false_positive(finding_id: str) -> None:
    """Labels a finding as a false positive in LATTICE."""
    qdrant = _get_qdrant()
    if not qdrant:
        logger.warning("Qdrant unavailable, skipping label_false_positive.")
        return

    try:
        # We need to update the payload of the existing point.
        point_id = _generate_id(finding_id)
        qdrant.set_payload(
            collection_name=COLLECTION_NAME,
            points=[point_id],
            payload={"false_positive": True},
        )
    except Exception as e:
        logger.warning(f"Failed to label false positive: {e}")
