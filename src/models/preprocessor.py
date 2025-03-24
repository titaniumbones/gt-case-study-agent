"""Preprocessing utilities for GivingTuesday campaign advisor using LlamaIndex."""

from typing import Dict, List, Optional, Union

from llama_index.core.llms import LLM
from pydantic import BaseModel, Field

from src.models.factory import create_cost_effective_model
from src.utils.logging import logger
from src.prompts import QUERY_ENHANCEMENT_PROMPT, QUERY_ANALYSIS_PROMPT


class QueryAnalysis(BaseModel):
    """Analysis of a user query."""

    enhanced_query: str = Field(..., description="Enhanced query for retrieval")
    key_themes: List[str] = Field(
        default_factory=list, description="Key themes in the query"
    )
    focus_areas: List[str] = Field(
        default_factory=list, description="Relevant focus areas"
    )
    search_keywords: List[str] = Field(
        default_factory=list, description="Keywords for searching"
    )
    quote_keywords: List[str] = Field(
        default_factory=list, description="Keywords for finding quotable content"
    )


class QueryPreprocessor:
    """Preprocessor for user queries.

    This class enhances user queries for better retrieval and analysis.
    """

    def __init__(self, model: Optional[LLM] = None):
        """Initialize the preprocessor.

        Args:
            model: Optional language model to use. If not provided, a default cost-effective
                model will be created based on configuration.
        """
        # Initialize language model
        self.llm = model or create_cost_effective_model()

    def enhance_query(self, query: str) -> str:
        """Enhance a user query for better retrieval.

        Args:
            query: Original user query.

        Returns:
            Enhanced query.
        """
        logger.debug(f"Enhancing query: {query}")

        # Use the centralized prompt from prompts.py
        prompt = QUERY_ENHANCEMENT_PROMPT.format(query=query)
        enhanced_query = self.llm.complete(prompt).text.strip()

        logger.debug(f"Enhanced query: {enhanced_query}")
        return enhanced_query

    def analyze_query(self, query: str) -> QueryAnalysis:
        """Analyze a user query to extract themes, focus areas, and keywords.

        Args:
            query: User query.

        Returns:
            Query analysis.
        """
        logger.debug(f"Analyzing query: {query}")

        # First enhance the query
        enhanced_query = self.enhance_query(query)

        # Use the centralized prompt from prompts.py
        prompt = QUERY_ANALYSIS_PROMPT.format(enhanced_query=enhanced_query)
        analysis_text = self.llm.complete(prompt).text

        # Parse analysis
        try:
            key_themes = []
            focus_areas = []
            search_keywords = []
            quote_keywords = []

            for line in analysis_text.split("\n"):
                line = line.strip()
                if line.startswith("Key Themes:"):
                    themes = line.replace("Key Themes:", "").strip()
                    key_themes = [theme.strip() for theme in themes.split(",") if theme.strip()]
                elif line.startswith("Focus Areas:"):
                    areas = line.replace("Focus Areas:", "").strip()
                    focus_areas = [area.strip() for area in areas.split(",") if area.strip()]
                elif line.startswith("Search Keywords:"):
                    keywords = line.replace("Search Keywords:", "").strip()
                    search_keywords = [
                        keyword.strip() for keyword in keywords.split(",") if keyword.strip()
                    ]
                elif line.startswith("Quote Keywords:"):
                    quotes = line.replace("Quote Keywords:", "").strip()
                    quote_keywords = [
                        quote.strip() for quote in quotes.split(",") if quote.strip()
                    ]

            # Create analysis object
            analysis = QueryAnalysis(
                enhanced_query=enhanced_query,
                key_themes=key_themes,
                focus_areas=focus_areas,
                search_keywords=search_keywords,
                quote_keywords=quote_keywords,
            )

            logger.debug(f"Query analysis: {analysis}")
            return analysis

        except Exception as e:
            logger.error(f"Error parsing query analysis: {e}")
            # Return basic analysis with just the enhanced query
            return QueryAnalysis(
                enhanced_query=enhanced_query,
                key_themes=[],
                focus_areas=[],
                search_keywords=[],
                quote_keywords=[],
            )