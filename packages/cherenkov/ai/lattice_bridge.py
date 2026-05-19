from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from sentence_transformers import SentenceTransformer
import uuid, logging, hashlib

QDRANT_URL = 'http://localhost:6333'
COLLECTION = 'cherenkov_findings'

def _ensure_collection(client: QdrantClient) -> None:
    try:
        client.get_collection(COLLECTION)
    except Exception:
        client.create_collection(
            COLLECTION,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )

async def embed_and_store(trace: dict) -> str:
    try:
        client = QdrantClient(url=QDRANT_URL, timeout=5)
        _ensure_collection(client)
        model = SentenceTransformer('all-MiniLM-L6-v2')
        text = str(trace.get('findings', trace.get('target', '')))
        vector = model.encode(text).tolist()

        # Deterministic hashing instead of python's hash()
        trace_id = str(trace.get('trace_id', str(uuid.uuid4())))
        point_id = int(hashlib.md5(trace_id.encode()).hexdigest(), 16) % ((1<<63)-1)

        client.upsert(COLLECTION,
            points=[PointStruct(id=point_id, vector=vector, payload=trace)])
        return str(point_id)
    except Exception as e:
        logging.warning('LATTICE embed failed: %s', e)
        return ''

async def query_similar_targets(target: str, limit: int = 5) -> list:
    try:
        client = QdrantClient(url=QDRANT_URL, timeout=5)
        model = SentenceTransformer('all-MiniLM-L6-v2')
        vector = model.encode(target).tolist()
        results = client.search(COLLECTION, query_vector=vector, limit=limit)
        return [r.payload for r in results]
    except Exception as e:
        logging.warning('LATTICE query failed: %s', e)
        return []

async def label_false_positive(finding_id: str) -> None:
    try:
        client = QdrantClient(url=QDRANT_URL, timeout=5)
        client.set_payload(COLLECTION,
            payload={'is_false_positive': True},
            points=[int(finding_id)])
    except Exception as e:
        logging.warning('LATTICE label failed: %s', e)
