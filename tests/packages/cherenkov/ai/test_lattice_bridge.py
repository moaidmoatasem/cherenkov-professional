import pytest
from unittest.mock import patch, MagicMock
import hashlib

@pytest.fixture
def mock_qdrant_encoder():
    with patch("cherenkov.ai.lattice_bridge._get_qdrant") as mock_get_qdrant, \
         patch("cherenkov.ai.lattice_bridge._get_encoder") as mock_get_encoder:

        mock_qdrant = MagicMock()
        mock_encoder = MagicMock()

        mock_get_qdrant.return_value = mock_qdrant
        mock_get_encoder.return_value = mock_encoder

        yield mock_qdrant, mock_encoder

from cherenkov.ai.lattice_bridge import embed_and_store, query_similar_targets, label_false_positive, COLLECTION_NAME, _generate_id

def test_embed_and_store(mock_qdrant_encoder):
    mock_qdrant, mock_encoder = mock_qdrant_encoder
    mock_encoder.encode.return_value = MagicMock(tolist=lambda: [0.1, 0.2, 0.3])

    trace = {"finding_id": "test-123", "title": "XSS", "description": "Reflected"}
    result = embed_and_store(trace)

    assert result == "test-123"
    mock_encoder.encode.assert_called_once_with("XSS Reflected")
    mock_qdrant.upsert.assert_called_once()
    kwargs = mock_qdrant.upsert.call_args[1]
    assert kwargs["collection_name"] == COLLECTION_NAME
    assert kwargs["points"][0].vector == [0.1, 0.2, 0.3]
    assert kwargs["points"][0].payload == trace
    assert kwargs["points"][0].id == _generate_id("test-123")

def test_query_similar_targets(mock_qdrant_encoder):
    mock_qdrant, mock_encoder = mock_qdrant_encoder
    mock_encoder.encode.return_value = MagicMock(tolist=lambda: [0.1, 0.2, 0.3])

    mock_result = MagicMock()
    mock_result.payload = {"finding_id": "test-123"}
    mock_qdrant.search.return_value = [mock_result]

    results = query_similar_targets("test target", limit=2)

    assert len(results) == 1
    assert results[0] == {"finding_id": "test-123"}
    mock_encoder.encode.assert_called_once_with("test target")
    mock_qdrant.search.assert_called_once()
    kwargs = mock_qdrant.search.call_args[1]
    assert kwargs["collection_name"] == COLLECTION_NAME
    assert kwargs["query_vector"] == [0.1, 0.2, 0.3]
    assert kwargs["limit"] == 2

def test_label_false_positive(mock_qdrant_encoder):
    mock_qdrant, _ = mock_qdrant_encoder

    label_false_positive("test-123")

    mock_qdrant.set_payload.assert_called_once()
    kwargs = mock_qdrant.set_payload.call_args[1]
    assert kwargs["collection_name"] == COLLECTION_NAME
    assert kwargs["payload"] == {"false_positive": True}
    assert kwargs["points"][0] == _generate_id("test-123")

def test_graceful_failures():
    with patch("cherenkov.ai.lattice_bridge._get_qdrant", return_value=None), \
         patch("cherenkov.ai.lattice_bridge._get_encoder", return_value=None):
        assert embed_and_store({"finding_id": "1"}) == ""
        assert query_similar_targets("test") == []
        # should not raise
        label_false_positive("1")
