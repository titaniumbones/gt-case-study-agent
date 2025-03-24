"""GivingTuesday Campaign Advisor model components."""

from typing import Dict, List, Optional, Union

from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel

from src.data.schema import CampaignAdvice, CaseStudy
from src.models.factory import create_reasoning_model
from src.models.preprocessor import QueryPreprocessor
from src.utils.config import config
from src.utils.logging import logger


class CampaignAdvisor:
    """GivingTuesday Campaign Advisor.

    This class provides campaign advice based on similar case studies.
    """

    def __init__(
        self,
        vectordb: Chroma,
        model: Optional[BaseChatModel] = None,
        preprocessor: Optional[QueryPreprocessor] = None,
        use_query_enhancement: bool = True,
    ):
        """Initialize the advisor.

        Args:
            vectordb: Vector database of case studies.
            model: Optional language model to use. If not provided, a default model
                will be created based on configuration.
            preprocessor: Optional query preprocessor. If not provided and
                use_query_enhancement is True, a default preprocessor will be created.
            use_query_enhancement: Whether to use query enhancement. Defaults to True.
        """
        self.vectordb = vectordb
        self.use_query_enhancement = use_query_enhancement

        # Initialize language model
        self.llm = model or create_reasoning_model()

        # Initialize preprocessor if needed
        self.preprocessor = None
        if use_query_enhancement:
            self.preprocessor = preprocessor or QueryPreprocessor()

    def get_relevant_case_studies(self, query: str, k: int = 5) -> List[Dict]:
        """Get relevant case studies for a query.

        Args:
            query: User query.
            k: Number of relevant case studies to retrieve.

        Returns:
            List of relevant case study metadata.
        """
        logger.debug(f"Getting relevant case studies for query: {query}")

        # Enhance query if needed
        search_query = query
        if self.use_query_enhancement and self.preprocessor:
            try:
                analysis = self.preprocessor.analyze_query(query)
                search_query = analysis.enhanced_query
                logger.debug(f"Using enhanced query: {search_query}")
            except Exception as e:
                logger.warning(f"Error enhancing query: {e}. Using original query.")

        # Search for relevant documents
        relevant_docs = self.vectordb.similarity_search(search_query, k=k)
        case_studies = [doc.metadata for doc in relevant_docs]

        return case_studies

    def generate_advice(self, query: str, case_studies: List[Dict]) -> CampaignAdvice:
        """Generate advice based on relevant case studies.

        Args:
            query: User query.
            case_studies: List of relevant case study metadata.

        Returns:
            Campaign advice.
        """
        logger.debug(f"Generating advice for query: {query}")

        # Create prompt template
        prompt = ChatPromptTemplate.from_template(
            """You are an expert advisor for GivingTuesday campaigns. Your job is to provide 
            helpful, actionable advice based on successful case studies.
            
            USER QUERY: {query}
            
            RELEVANT CASE STUDIES:
            {case_studies}
            
            Based on these case studies, provide specific, actionable advice for the user's query.
            Focus on practical strategies that have been proven effective in similar campaigns.
            Include references to specific case studies that support your advice.
            
            FORMAT YOUR RESPONSE AS FOLLOWS:
            1. Start with a brief introduction to establish context
            2. Provide 3-5 specific, actionable recommendations
            3. For each recommendation:
               - Explain its relevance
               - Include at least one brief quote or specific example from a case study
               - Explicitly mention the campaign name (e.g., "As demonstrated by the [Campaign Name]...")
               - Format campaign references in bold or with quotes for emphasis
            4. End with a brief conclusion
            
            IMPORTANT: 
            - Be specific and practical with each piece of advice
            - For EVERY recommendation, include a direct quote or specific example from the case studies
            - ALWAYS include the exact name of the relevant campaign for each example
            - Use phrases like "According to [Campaign Name]..." or "The [Campaign Name] showed that..."
            - Put campaign names in quotes or bold (using markdown) for emphasis
            - Focus on strategies that have been proven successful in similar contexts
            - Adapt the advice to the user's specific query
            """
        )

        # Format case studies for the prompt
        case_studies_text = ""
        references = []

        for i, cs in enumerate(case_studies, 1):
            case_study_name = cs.get("case_study_entry", "Unnamed Case Study")
            case_studies_text += f"{i}. CASE STUDY: {case_study_name}\n"
            case_studies_text += f"   COUNTRY: {cs.get('country', 'Unknown')}\n"

            # Add full story if available - good source for quotes
            if cs.get("full_story"):
                case_studies_text += f"   FULL STORY: {cs.get('full_story')}\n"

            if cs.get("focus_area"):
                case_studies_text += f"   FOCUS AREA: {cs.get('focus_area')}\n"

            if cs.get("goals"):
                case_studies_text += f"   GOALS: {cs.get('goals')}\n"

            if cs.get("key_activities"):
                case_studies_text += f"   KEY ACTIVITIES: {cs.get('key_activities')}\n"

            # Add clear section for quotable content
            if cs.get("outcomes"):
                case_studies_text += f"   QUOTABLE OUTCOMES: {cs.get('outcomes')}\n"

            if cs.get("main_theme"):
                case_studies_text += f"   MAIN THEME: {cs.get('main_theme')}\n"

            # Add subtheme if available
            if cs.get("subtheme"):
                case_studies_text += f"   SUBTHEME: {cs.get('subtheme')}\n"

            # Add a section to highlight the campaign name for citation
            case_studies_text += f'   REFERENCE AS: "{case_study_name}"\n'

            case_studies_text += "\n"

            # Add to references
            references.append(case_study_name)

        # Create chain
        chain = prompt | self.llm | StrOutputParser()

        # Generate advice
        advice_text = chain.invoke({"query": query, "case_studies": case_studies_text})

        # Create advice object
        advice = CampaignAdvice(advice=advice_text, references=references)

        return advice

    def get_advice(self, query: str) -> CampaignAdvice:
        """Get advice for a user query.

        Args:
            query: User query about campaign advice.

        Returns:
            Campaign advice.
        """
        # Get relevant case studies
        case_studies = self.get_relevant_case_studies(query)

        # Generate advice
        advice = self.generate_advice(query, case_studies)

        return advice
