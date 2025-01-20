import pytest
import networkx as nx
from unittest.mock import patch, mock_open
import json
from src.model.graph import create_graph

@pytest.fixture
def sample_translated_content():
    """Fixture to provide sample translated JSON content."""
    return {
        "url": "https://example.com",
        "headers": ["Header1", "Header2"],
        "paragraphs": ["Paragraph1 explaining Header1", "Paragraph2 explaining Header2"]
    }

def test_create_graph(sample_translated_content):
    """Test the create_graph function with valid content."""
    # mock the open function to return the sample content
    mock_file_content = json.dumps(sample_translated_content)
    with patch("builtins.open", mock_open(read_data=mock_file_content)):
        G = create_graph("mock_input.json")

    # assert that the graph is created
    assert G is not None
    assert isinstance(G, nx.MultiDiGraph)

    # assert nodes are correctly added
    headers = sample_translated_content["headers"]
    paragraphs = sample_translated_content["paragraphs"]
    for header in headers:
        assert header in G.nodes
        assert G.nodes[header]["type"] == "header"
    for paragraph in paragraphs:
        assert paragraph in G.nodes
        assert G.nodes[paragraph]["type"] == "paragraph"

    # assert "explains" edges are correctly added
    for header, paragraph in zip(headers, paragraphs):
        edges = G.get_edge_data(paragraph, header)
        assert edges is not None
        assert any(edge["relationship"] == "explains" for edge in edges.values())

    # assert "related_to" edges are added
    for node_a in headers + paragraphs:
        for node_b in headers + paragraphs:
            if node_a != node_b:
                edges = G.get_edge_data(node_a, node_b)
                if edges:  # only check if edges exist
                    assert all(edge["relationship"] in {"explains", "related_to"} for edge in edges.values())


def test_create_graph_with_empty_content():
    """Test the create_graph function with empty content."""
    empty_content = {"url": "https://example.com", "headers": [], "paragraphs": []}

    # mock the open function to return the empty content
    mock_file_content = json.dumps(empty_content)
    with patch("builtins.open", mock_open(read_data=mock_file_content)):
        G = create_graph("mock_input.json")

    # assert the graph is created but contains no nodes
    assert G is not None
    assert isinstance(G, nx.DiGraph)
    assert len(G.nodes) == 0
    assert len(G.edges) == 0

def test_create_graph_invalid_input():
    """Test the create_graph function with invalid input."""
    # mock the open function to raise a JSON decode error
    with patch("builtins.open", mock_open(read_data="Invalid JSON")):
        G = create_graph("mock_input.json")

    # ssert the function returns None on error
    assert G is None
