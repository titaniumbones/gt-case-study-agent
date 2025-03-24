"""Preprocessing utilities for GivingTuesday campaign advisor using LlamaIndex."""

from typing import Dict, List, Optional, Union

from llama_index.core.llms import LLM
from pydantic import BaseModel, Field

from src.models.factory import create_cost_effective_model
from src.utils.logging import logger


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

        # Create the prompt for query enhancement
        prompt_template = """You are a query enhancement assistant for a GivingTuesday campaign advisor system.
        Your task is to enhance the user's query to improve retrieval of relevant campaign examples.
        
        USER QUERY: {query}
        
        Please enhance this query by:
        1. Expanding abbreviations
        2. Adding relevant synonyms
        3. Clarifying ambiguous terms
        4. Adding key GivingTuesday concepts that are implied but not stated
        5. Including terms that would help find quotes and specific examples from campaigns
        6. Adding terminology that would help find success stories and quotable campaign outcomes
        
        Provide ONLY the enhanced query text without any explanations or additional text.
        """

        # Use the LLM to enhance the query
        prompt = prompt_template.format(query=query)
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

        # Create the prompt for query analysis
        prompt_template = """You are a query analysis assistant for a GivingTuesday campaign advisor system.
        Your task is to analyze the user's query to extract key themes, focus areas, search keywords, and identify quotable content.
        
        ENHANCED QUERY: {enhanced_query}
        
        Please analyze this query and extract:
        1. Key themes related to GivingTuesday campaigns
        2. Relevant focus areas (e.g., fundraising, volunteer mobilization, social media)
        3. Specific keywords that would be useful for searching campaign examples
        4. Terms that would help identify quotable success stories, statistics, or testimonials
        5. Words related to specific campaign tactics or strategies that should be highlighted
        
        Format your response as follows:
        Key Themes: theme1, theme2, theme3
        Focus Areas: area1, area2, area3
        Search Keywords: keyword1, keyword2, keyword3, keyword4
        Quote Keywords: quote1, quote2, quote3, quote4
        
        Be specific and thorough in your analysis. The Quote Keywords will be especially important for finding content that can be directly quoted in our response.
        """

        # Use the LLM to analyze the query
        prompt = prompt_template.format(enhanced_query=enhanced_query)
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