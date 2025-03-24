"""Tests for the LlamaIndex integration."""

import pytest
from unittest.mock import MagicMock, patch

from src.data.loader import get_or_create_vector_store_index
from src.models.advisor import CampaignAdvisor
from src.models.factory import create_reasoning_model


@pytest.fixture
def mock_vector_store_index():
    """Create a mock vector store index."""
    mock_index = MagicMock()
    mock_retriever = MagicMock()
    mock_index._vector_store = MagicMock()
    mock_node = MagicMock()
    mock_node.metadata = {"case_study_entry": "Test Case Study", "country": "Test Country"}
    mock_node.text = "Test content"
    mock_retriever.retrieve.return_value = [mock_node]
    
    # Make retriever accessible via index
    mock_index.as_retriever.return_value = mock_retriever
    
    return mock_index


@patch("src.data.loader.get_or_create_vector_store_index")
@patch("src.models.factory.create_reasoning_model")
def test_campaign_advisor_get_relevant_case_studies(mock_create_model, mock_get_index, mock_vector_store_index):
    """Test the CampaignAdvisor.get_relevant_case_studies method."""
    # Set up mocks
    mock_get_index.return_value = mock_vector_store_index
    mock_model = MagicMock()
    mock_create_model.return_value = mock_model
    
    # Create the advisor
    advisor = CampaignAdvisor(mock_vector_store_index, model=mock_model)
    
    # Call the method
    results = advisor.get_relevant_case_studies("test query")
    
    # Check results
    assert len(results) > 0
    assert "case_study_entry" in results[0]
    assert results[0]["case_study_entry"] == "Test Case Study"


@patch("src.data.loader.get_or_create_vector_store_index")
@patch("src.models.factory.create_reasoning_model")
def test_campaign_advisor_generate_advice(mock_create_model, mock_get_index, mock_vector_store_index):
    """Test the CampaignAdvisor.generate_advice method."""
    # Set up mocks
    mock_get_index.return_value = mock_vector_store_index
    mock_model = MagicMock()
    mock_model.complete.return_value.text = "Test advice"
    mock_create_model.return_value = mock_model
    
    # Create the advisor
    advisor = CampaignAdvisor(mock_vector_store_index, model=mock_model)
    
    # Call the method
    case_studies = [
        {"case_study_entry": "Test Study 1", "country": "Country 1"},
        {"case_study_entry": "Test Study 2", "country": "Country 2"},
    ]
    advice = advisor.generate_advice("test query", case_studies)
    
    # Check results
    assert advice.advice == "Test advice"
    assert len(advice.references) == 2
    assert "Test Study 1" in advice.references


@patch("src.data.loader.get_or_create_vector_store_index")
@patch("src.models.factory.create_reasoning_model")
def test_campaign_advisor_get_advice(mock_create_model, mock_get_index, mock_vector_store_index):
    """Test the CampaignAdvisor.get_advice method."""
    # Set up mocks
    mock_get_index.return_value = mock_vector_store_index
    mock_model = MagicMock()
    mock_model.complete.return_value.text = "Test advice"
    mock_create_model.return_value = mock_model
    
    # Create advisor with mocks
    advisor = CampaignAdvisor(mock_vector_store_index, model=mock_model)
    
    # Mock specific methods
    advisor.get_relevant_case_studies = MagicMock(return_value=[
        {"case_study_entry": "Test Study", "country": "Test Country"}
    ])
    
    # Call method
    advice = advisor.get_advice("test query")
    
    # Check results
    assert advice.advice == "Test advice"
    assert len(advice.references) == 1
    assert "Test Study" in advice.references