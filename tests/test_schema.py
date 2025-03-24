"""Tests for data schemas."""

import pytest

from src.data.schema import CampaignAdvice, CaseStudy


def test_case_study_creation():
    """Test creating a case study object."""
    # Create a minimal case study
    case_study = CaseStudy(
        case_study_entry="Test Case Study",
        country="Test Country"
    )
    
    assert case_study.case_study_entry == "Test Case Study"
    assert case_study.country == "Test Country"


def test_case_study_get_content_for_embedding():
    """Test getting content for embedding."""
    # Create a case study with some fields
    case_study = CaseStudy(
        case_study_entry="Test Case Study",
        country="Test Country",
        full_story="This is a test case study.",
        goals="The goal is to test the schema.",
        main_theme="Testing"
    )
    
    # Get content for embedding
    content = case_study.get_content_for_embedding()
    
    # Check that the content contains the fields
    assert "Test Case Study" in content
    assert "Test Country" in content
    assert "This is a test case study." in content
    assert "The goal is to test the schema." in content
    assert "Testing" in content


def test_campaign_advice_creation():
    """Test creating a campaign advice object."""
    # Create a campaign advice
    advice = CampaignAdvice(
        advice="This is some test advice.",
        references=["Test Case Study 1", "Test Case Study 2"]
    )
    
    assert advice.advice == "This is some test advice."
    assert len(advice.references) == 2
    assert "Test Case Study 1" in advice.references
    assert "Test Case Study 2" in advice.references
