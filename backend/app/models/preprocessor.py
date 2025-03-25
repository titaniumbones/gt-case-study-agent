from typing import Any
import logging

from app.utils.prompts import QUERY_ENHANCEMENT_PROMPT

logger = logging.getLogger(__name__)

class QueryPreprocessor:
    """
    Enhances user queries to improve retrieval quality.
    Uses a cost-effective model to expand the query with additional relevant terms.
    """
    
    def __init__(self, llm: Any):
        """
        Initialize the query preprocessor.
        
        Args:
            llm: Language model provider to use for query enhancement
        """
        self.llm = llm
        logger.info("Query preprocessor initialized")
    
    def enhance_query(self, original_query: str) -> str:
        """
        Enhance a user query to improve retrieval results.
        
        Args:
            original_query: The user's original query
            
        Returns:
            Enhanced query with additional context and search terms
        """
        if not original_query.strip():
            return original_query
        
        try:
            # Format the enhancement prompt
            prompt = QUERY_ENHANCEMENT_PROMPT.format(query=original_query)
            
            # Get enhanced query from LLM
            response = self.llm.complete(prompt)
            
            # Extract text from response object if needed
            if hasattr(response, 'text'):
                enhanced_query = response.text
            else:
                enhanced_query = str(response)
            
            if not enhanced_query.strip():
                logger.warning("Query enhancement returned empty result")
                return original_query
                
            logger.info(f"Enhanced query: {enhanced_query}")
            return enhanced_query
            
        except Exception as e:
            logger.error(f"Error enhancing query: {str(e)}")
            # Fall back to original query on error
            return original_query