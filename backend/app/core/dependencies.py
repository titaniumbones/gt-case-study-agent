from typing import Generator
from functools import lru_cache
import logging

from app.models.advisor import CampaignAdvisor
from app.models.factory import create_advisor
from app.core.config import settings

logger = logging.getLogger(__name__)

@lru_cache()
def get_campaign_advisor() -> CampaignAdvisor:
    """
    Create and cache the campaign advisor instance.
    Uses LRU cache to avoid creating a new instance for each request.
    """
    logger.info("Creating campaign advisor instance")
    
    # Validate API keys
    if not settings.ANTHROPIC_API_KEY or not settings.OPENAI_API_KEY:
        logger.warning("API keys not set. Both ANTHROPIC_API_KEY and OPENAI_API_KEY must be set.")
    
    return create_advisor(
        case_study_file=settings.CASE_STUDY_FILE,
        vector_db_path=settings.VECTOR_DB_PATH,
        fast_model_name=settings.FAST_MODEL_NAME,
        detailed_model_name=settings.DETAILED_MODEL_NAME
    )

def get_advisor() -> Generator[CampaignAdvisor, None, None]:
    """Dependency to get the campaign advisor instance."""
    advisor = get_campaign_advisor()
    yield advisor