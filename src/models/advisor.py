"""GivingTuesday Campaign Advisor model components using LlamaIndex."""

from typing import Dict, List, Optional, Union

from llama_index.core.llms import LLM
from llama_index.core.indices.vector_store import VectorStoreIndex
from llama_index.core.response_synthesizers import ResponseMode
from llama_index.core.retrievers import VectorIndexRetriever

from src.data.schema import CampaignAdvice
from src.models.factory import create_reasoning_model
from src.models.preprocessor import QueryPreprocessor
from src.utils.config import config
from src.utils.logging import logger
from src.prompts import ADVICE_GENERATION_PROMPT, FAST_MODE_ADVICE_PROMPT


class CampaignAdvisor:
    """GivingTuesday Campaign Advisor.

    This class provides campaign advice based on similar case studies.
    """

    def __init__(
        self,
        index: VectorStoreIndex,
        model: Optional[LLM] = None,
        preprocessor: Optional[QueryPreprocessor] = None,
        use_query_enhancement: bool = True,
    ):
        """Initialize the advisor.

        Args:
            index: Vector store index of case studies.
            model: Optional language model to use. If not provided, a default model
                will be created based on configuration.
            preprocessor: Optional query preprocessor. If not provided and
                use_query_enhancement is True, a default preprocessor will be created.
            use_query_enhancement: Whether to use query enhancement. Defaults to True.
        """
        self.index = index
        self.use_query_enhancement = use_query_enhancement

        # Initialize language model
        self.llm = model or create_reasoning_model()
        
        # Check if this is a fast mode (for prompt selection)
        # We'll check based on the name of the model since type checking is unreliable
        self.is_fast_mode = False
        
        # If we have a model, check if it matches any patterns for cost-effective models
        if model:
            model_identifiers = ["haiku", "cost-effective", "fast"]
            model_name = getattr(model, "model", "").lower()
            self.is_fast_mode = any(identifier in model_name for identifier in model_identifiers)

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

        # Create retriever with top-k
        retriever = VectorIndexRetriever(
            index=self.index,
            similarity_top_k=k,
        )

        # Retrieve nodes
        nodes = retriever.retrieve(search_query)
        
        # Extract metadata from nodes
        case_studies = []
        for node in nodes:
            if hasattr(node, 'metadata') and node.metadata:
                case_studies.append(node.metadata)
                
        logger.info(f"Retrieved {len(case_studies)} case studies for query")
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

        # Select the appropriate prompt based on fast mode
        if self.is_fast_mode:
            prompt_template = FAST_MODE_ADVICE_PROMPT
        else:
            prompt_template = ADVICE_GENERATION_PROMPT

        # Format the prompt with query and case studies
        prompt = prompt_template.format(
            query=query,
            case_studies=case_studies_text
        )

        # Generate advice using the LLM
        advice_text = self.llm.complete(prompt).text

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
