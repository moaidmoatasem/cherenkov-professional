import pytest
from unittest.mock import patch, MagicMock
from cherenkov.ai.lattice_bridge import embed_and_store, query_similar_targets, label_false_positive

@pytest.fixture
def mock_qdrant():
    with patch('cherenkov.ai.lattice_bridge.QdrantClient') as MockClient:
        yield MockClient

@pytest.fixture
def mock_sentence_transformer():
    with patch('cherenkov.ai.lattice_bridge.SentenceTransformer') as MockModel:
        mock_instance = MockModel.return_value
        mock_instance.encode.return_value = MagicMock(tolist=lambda: [0.1, 0.2, 0.3])
        yield MockModel

@pytest.mark.asyncio
async def test_embed_and_store_success(mock_qdrant, mock_sentence_transformer):
    mock_client_instance = mock_qdrant.return_value
    mock_client_instance.get_collection.return_value = True

    trace = {'trace_id': 'test_trace_123', 'target': 'http://example.com'}
    result = await embed_and_store(trace)

    assert result != ''
    mock_client_instance.upsert.assert_called_once()
    assert mock_sentence_transformer.return_value.encode.called

@pytest.mark.asyncio
async def test_embed_and_store_failure(mock_qdrant):
    mock_qdrant.side_effect = Exception("Connection Error")

    trace = {'trace_id': 'test_trace_123', 'target': 'http://example.com'}
    result = await embed_and_store(trace)

    assert result == ''

@pytest.mark.asyncio
async def test_query_similar_targets_success(mock_qdrant, mock_sentence_transformer):
    mock_client_instance = mock_qdrant.return_value

    # Mocking the search results
    mock_result_1 = MagicMock(payload={'target': 'http://example.com'})
    mock_result_2 = MagicMock(payload={'target': 'http://example.org'})
    mock_client_instance.search.return_value = [mock_result_1, mock_result_2]

    results = await query_similar_targets('http://example.com')

    assert len(results) == 2
    assert results[0]['target'] == 'http://example.com'
    assert results[1]['target'] == 'http://example.org'
    mock_client_instance.search.assert_called_once()

@pytest.mark.asyncio
async def test_query_similar_targets_failure(mock_qdrant):
    mock_qdrant.side_effect = Exception("Connection Error")

    results = await query_similar_targets('http://example.com')

    assert results == []

@pytest.mark.asyncio
async def test_label_false_positive_success(mock_qdrant):
    mock_client_instance = mock_qdrant.return_value

    await label_false_positive('123456789')

    mock_client_instance.set_payload.assert_called_once()
    kwargs = mock_client_instance.set_payload.call_args[1]
    assert kwargs['payload'] == {'is_false_positive': True}
    assert kwargs['points'] == [123456789]

@pytest.mark.asyncio
async def test_label_false_positive_failure(mock_qdrant):
    mock_qdrant.side_effect = Exception("Connection Error")

    # Should not raise an exception, just log a warning
    await label_false_positive('123456789')
