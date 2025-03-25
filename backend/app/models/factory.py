from typing import Optional
import os
import logging
from llama_index.llms.anthropic import Anthropic
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core.node_parser import SentenceSplitter
from llama_index.vector_stores.chroma import ChromaVectorStore
from chromadb import PersistentClient
import chromadb
import shutil

from app.models.advisor import CampaignAdvisor
from app.models.preprocessor import QueryPreprocessor
from app.utils.data import load_case_studies_from_csv
from app.core.config import settings

logger = logging.getLogger(__name__)

def create_advisor(
    case_study_file: str = "data/case-study-inventory.csv",
    vector_db_path: str = "vectordb",
    recreate: bool = False,
    fast_model_name: str = "claude-3-haiku-20240307",
    detailed_model_name: str = "claude-3-sonnet-20240229",
) -> CampaignAdvisor:
    """
    Creates a CampaignAdvisor instance with the appropriate components.
    
    Args:
        case_study_file: Path to the CSV file with case studies
        vector_db_path: Path to store the vector database
        recreate: Whether to recreate the vector store index
        fast_model_name: Name of the fast model to use
        detailed_model_name: Name of the detailed model to use
        
    Returns:
        Initialized CampaignAdvisor
    """
    # Create model providers
    detailed_model = Anthropic(
        api_key=settings.ANTHROPIC_API_KEY,
        model=detailed_model_name
    )
    
    fast_model = Anthropic(
        api_key=settings.ANTHROPIC_API_KEY,
        model=fast_model_name
    )
    
    # Create query preprocessor
    query_preprocessor = QueryPreprocessor(
        llm=fast_model
    )
    
    # Check if vector database already exists
    vector_store_exists = os.path.exists(vector_db_path) and len(os.listdir(vector_db_path)) > 0
    
    if vector_store_exists and not recreate:
        logger.info(f"Loading existing vector store from {vector_db_path}")
        
        # Create advisor from existing vector store
        return CampaignAdvisor.from_case_studies(
            vector_store_dir=vector_db_path,
            detailed_model_provider=detailed_model,
            fast_model_provider=fast_model,
            query_preprocessor=query_preprocessor
        )
    
    # We need to create a new vector store
    logger.info(f"Creating new vector store from {case_study_file}")
    
    # Load case studies from CSV
    documents = load_case_studies_from_csv(case_study_file)
    
    if not documents:
        raise ValueError(f"No case studies found in {case_study_file}")
    
    # Create text splitter
    text_splitter = SentenceSplitter(
        chunk_size=512,
        chunk_overlap=50
    )
    
    # Create embedding model
    embed_model = OpenAIEmbedding(
        api_key=settings.OPENAI_API_KEY,
        model="text-embedding-3-small"
    )
    
    # Set up vector store
    os.makedirs(vector_db_path, exist_ok=True)
    
    # Clear existing collection if recreating
    if recreate and vector_store_exists:
        logger.info("Recreating vector store - clearing existing data")
        try:
            # Remove the entire directory to ensure clean state
            shutil.rmtree(vector_db_path)
            os.makedirs(vector_db_path, exist_ok=True)
        except Exception as e:
            logger.warning(f"Error clearing vector store directory: {e}")
    
    # Create new Chroma collection
    chroma_client = PersistentClient(vector_db_path)
    chroma_collection = chroma_client.get_or_create_collection("case_studies")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    
    # Create storage context
    storage_context = StorageContext.from_defaults(
        vector_store=vector_store
    )
    
    # Create index
    logger.info(f"Indexing {len(documents)} documents with embedding model")
    index = VectorStoreIndex.from_documents(
        documents=documents,
        storage_context=storage_context,
        transformations=[text_splitter],
        embed_model=embed_model,
        show_progress=True,
    )
    
    logger.info(f"Vector store created with {len(documents)} case studies")
    
    # Create and return the advisor
    return CampaignAdvisor(
        index=index,
        detailed_model_provider=detailed_model,
        fast_model_provider=fast_model,
        query_preprocessor=query_preprocessor
    )