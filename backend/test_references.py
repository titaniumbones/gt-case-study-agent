"""
Test script to verify reference handling in the backend.
"""

import os
import logging
from dotenv import load_dotenv
from app.models.factory import create_advisor

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def test_references():
    """Test the reference handling functionality."""
    # Check for API keys
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    
    if not anthropic_key or not openai_key:
        logger.error("Missing API keys. Please set ANTHROPIC_API_KEY and OPENAI_API_KEY in .env file")
        return
    
    # Create the advisor with recreate=True to ensure we have the latest changes
    logger.info("Creating advisor with recreate=True")
    advisor = create_advisor(
        case_study_file="../data/case-study-inventory.csv",
        vector_db_path="vectordb",
        recreate=True
    )
    
    # Test a query to see what references we get
    test_query = "How can I engage volunteers for my GivingTuesday campaign?"
    logger.info(f"Testing query: {test_query}")
    
    result = advisor.get_advice(test_query, fast_mode=True)
    
    # Log the references
    logger.info(f"Number of references: {len(result.get('references', []))}")
    for i, ref in enumerate(result.get('references', [])):
        logger.info(f"Reference {i+1}:")
        logger.info(f"  Organization: {ref.get('organization', 'Unknown')}")
        logger.info(f"  Campaign: {ref.get('campaign_name', 'Unknown')}")
        logger.info(f"  Content length: {len(ref.get('content', ''))}")
        logger.info(f"  ID: {ref.get('id', 'No ID')}")
    
    logger.info("Test completed successfully")

if __name__ == "__main__":
    test_references()