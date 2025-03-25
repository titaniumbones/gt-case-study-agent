from typing import Dict, List, Optional, Any
import logging
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.vector_stores.chroma import ChromaVectorStore
from chromadb import PersistentClient

from app.models.preprocessor import QueryPreprocessor
from app.utils.prompts import ADVICE_GENERATION_PROMPT, FAST_MODE_ADVICE_PROMPT

logger = logging.getLogger(__name__)

class CampaignAdvisor:
    """
    Main advisor class that provides campaign advice based on relevant case studies.
    """
    
    def __init__(
        self,
        index: VectorStoreIndex,
        detailed_model_provider: Any,
        fast_model_provider: Any,
        query_preprocessor: Optional[QueryPreprocessor] = None,
        retriever_top_k: int = 5,
    ):
        """
        Initialize the campaign advisor.
        
        Args:
            index: Vector store index for case studies
            detailed_model_provider: Primary LLM provider (Claude 3.7 Sonnet)
            fast_model_provider: Fast LLM provider (Claude 3.5 Haiku)
            query_preprocessor: Optional query preprocessor to enhance queries
            retriever_top_k: Number of case studies to retrieve
        """
        self.index = index
        self.detailed_model = detailed_model_provider
        self.fast_model = fast_model_provider
        self.query_preprocessor = query_preprocessor
        self.retriever_top_k = retriever_top_k
        
        # Create retriever
        self.retriever = VectorIndexRetriever(
            index=self.index,
            similarity_top_k=self.retriever_top_k
        )
        
        logger.info(f"Campaign advisor initialized with top_k={retriever_top_k}")
    
    def get_advice(self, query: str, fast_mode: bool = False) -> Dict[str, Any]:
        """
        Get advice for a campaign query.
        
        Args:
            query: The user's question about GivingTuesday campaigns
            fast_mode: Whether to use the fast model (Claude 3.5 Haiku)
            
        Returns:
            Dictionary containing advice and referenced case studies
        """
        # Preprocess the query if preprocessor is available
        if self.query_preprocessor and not fast_mode:
            enhanced_query = self.query_preprocessor.enhance_query(query)
            logger.info(f"Enhanced query: {enhanced_query}")
        else:
            enhanced_query = query
            
        # Retrieve relevant case studies
        nodes = self.retriever.retrieve(enhanced_query)
        
        if not nodes:
            logger.warning(f"No case studies found for query: {enhanced_query}")
            return {
                "advice": "I couldn't find any relevant case studies to address your question. "
                          "Please try rephrasing or ask a different question about GivingTuesday campaigns.",
                "references": []
            }
        
        # Extract case study texts and references
        case_studies_text = "\n\n".join([node.get_content() for node in nodes])
        
        # Log the nodes for debugging
        logger.info(f"Retrieved {len(nodes)} nodes")
        for i, node in enumerate(nodes):
            logger.info(f"Node {i}: ID={node.node_id}, Metadata={node.metadata}")
        
        # Create detailed references with full content for modal display
        references = []
        for node in nodes:
            organization = node.metadata.get('organization', 'Unknown Organization')
            campaign_name = node.metadata.get('campaign_name', 'Unknown Campaign')
            content = node.get_content()
            
            # Debug log the reference data
            logger.info(f"Creating reference: org={organization}, campaign={campaign_name}, content_length={len(content)}")
            
            references.append({
                "title": f"{organization} - {campaign_name}",
                "organization": organization,
                "campaign_name": campaign_name,
                "content": content,
                "id": node.node_id  # Include node_id as a unique identifier
            })
        
        # Select model and prompt based on mode
        if fast_mode:
            model = self.fast_model
            prompt_template = FAST_MODE_ADVICE_PROMPT
            logger.info("Using fast mode with Claude 3.5 Haiku")
        else:
            model = self.detailed_model
            prompt_template = ADVICE_GENERATION_PROMPT
            logger.info("Using detailed mode with Claude 3.7 Sonnet")
        
        # Format the prompt
        prompt = prompt_template.format(
            query=enhanced_query,
            case_studies=case_studies_text
        )
        
        # Generate advice - handle CompletionResponse objects 
        response = model.complete(prompt)
        
        # Extract the text from the CompletionResponse if it's not already a string
        if hasattr(response, 'text'):
            advice = response.text
        else:
            advice = str(response)
        
        logger.info(f"Returning {len(references)} references")
        
        # For testing - add some sample references if none were found
        if not references:
            logger.warning("No real references found, adding sample references for testing")
            references = [
                {
                    "title": "Sample Organization - Test Campaign 1",
                    "organization": "Sample Organization",
                    "campaign_name": "Test Campaign 1",
                    "content": "# Sample Organization: Test Campaign 1\n\n## Description\nThis is a sample campaign for testing purposes.\n\n## Strategies\nUsed social media effectively.\n\n## Results\nRaised $10,000 for the cause.",
                    "id": "sample-1"
                },
                {
                    "title": "Test Nonprofit - Sample Campaign 2",
                    "organization": "Test Nonprofit",
                    "campaign_name": "Sample Campaign 2",
                    "content": "# Test Nonprofit: Sample Campaign 2\n\n## Description\nAnother sample to ensure the interface works.\n\n## Strategies\nEngaged volunteers effectively.\n\n## Results\nIncreased donor base by 20%.",
                    "id": "sample-2"
                }
            ]
        
        return {
            "advice": advice,
            "references": references
        }
    
    @classmethod
    def from_case_studies(
        cls,
        vector_store_dir: str,
        detailed_model_provider: Any,
        fast_model_provider: Any,
        query_preprocessor: Optional[QueryPreprocessor] = None,
        retriever_top_k: int = 5,
    ) -> "CampaignAdvisor":
        """
        Create advisor from an existing vector store.
        
        Args:
            vector_store_dir: Directory containing Chroma vector store
            detailed_model_provider: Primary LLM provider
            fast_model_provider: Fast LLM provider
            query_preprocessor: Optional query preprocessor
            retriever_top_k: Number of case studies to retrieve
            
        Returns:
            Initialized CampaignAdvisor
        """
        # Load the existing vector store
        chroma_client = PersistentClient(vector_store_dir)
        chroma_collection = chroma_client.get_or_create_collection("case_studies")
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        
        # Create storage context and index
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex.from_vector_store(
            vector_store=vector_store,
            storage_context=storage_context,
        )
        
        return cls(
            index=index,
            detailed_model_provider=detailed_model_provider,
            fast_model_provider=fast_model_provider,
            query_preprocessor=query_preprocessor,
            retriever_top_k=retriever_top_k,
        )