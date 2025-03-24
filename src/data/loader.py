"""Data loading and processing utilities for GivingTuesday campaign case studies using LlamaIndex."""

import csv
from pathlib import Path
from typing import Dict, List, Optional, Union, Any

import pandas as pd
from tqdm import tqdm

from llama_index.core.schema import Document, TextNode
from llama_index.core.node_parser import SentenceSplitter
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.indices.vector_store import VectorStoreIndex
from llama_index.core.vector_stores.types import VectorStore
from llama_index.core.storage.storage_context import StorageContext
import chromadb

from src.data.schema import CaseStudy
from src.models.factory import create_embedding_model
from src.utils.config import config
from src.utils.logging import logger


def load_case_studies(file_path: Optional[Path] = None) -> List[CaseStudy]:
    """Load case studies from CSV file.

    Args:
        file_path: Path to the CSV file. Defaults to value in config.

    Returns:
        List of CaseStudy objects.
    """
    file_path = file_path or config.case_study_file

    logger.info(f"Loading case studies from {file_path}")

    try:
        # Check if file exists
        if not Path(file_path).exists():
            logger.error(f"Case study file not found: {file_path}")
            logger.error(f"Current working directory: {Path.cwd()}")
            return []

        logger.info(f"Reading CSV file from: {file_path} (absolute: {Path(file_path).absolute()})")

        # Try different encoding options if needed
        try:
            # First try with default encoding
            df = pd.read_csv(file_path)
        except UnicodeDecodeError:
            # If that fails, try with UTF-8 encoding
            logger.info("Retrying with UTF-8 encoding")
            df = pd.read_csv(file_path, encoding="utf-8")
        except Exception as e:
            # If that fails, try with latin-1 encoding
            logger.info(f"Retrying with latin-1 encoding after error: {e}")
            df = pd.read_csv(file_path, encoding="latin-1")

        logger.info(f"CSV file read successfully. Shape: {df.shape}")

        # Log column names for debugging
        logger.info(f"CSV columns: {df.columns.tolist()}")

        # Handle BOM character that might be present in CSV headers
        fixed_columns = []
        for col in df.columns:
            # Remove BOM character if present
            if col.startswith("\ufeff"):
                fixed_col = col.replace("\ufeff", "")
                logger.info(f"Fixed column name: '{col}' -> '{fixed_col}'")
                fixed_columns.append(fixed_col)
            else:
                fixed_columns.append(col)

        # Rename columns if any were fixed
        if df.columns.tolist() != fixed_columns:
            df.columns = fixed_columns
            logger.info("Fixed column names with BOM characters")

        # Map DataFrame column names to CaseStudy model fields (case-insensitive)
        column_mapping = {}

        # Define the mapping we're looking for (all lowercase for case-insensitive matching)
        desired_mapping = {
            "casestudy entry": "case_study_entry",
            "country": "country",
            "full story": "full_story",
            "region": "region",
            "local region (if applicable)/area/institution name": "local_region",
            "focus area/ cause/participating category": "focus_area",
            "lead/institution name": "lead_name",
            "date joined/ activity happened": "date",
            "links to materials": "links",
            "goals (what are they trying to do)": "goals",
            "key activities": "key_activities",
            "outcomes/ results (if applicable)": "outcomes",
            "contact": "contact",
            "main theme": "main_theme",
            "subtheme": "subtheme",
            "gt related themes/subthemes": "gt_themes",
            "notes": "notes",
        }

        # Try to match columns case-insensitive
        for col in df.columns:
            col_lower = col.lower()
            if col_lower in desired_mapping:
                column_mapping[col] = desired_mapping[col_lower]
                logger.debug(f"Mapped column: '{col}' -> '{desired_mapping[col_lower]}'")

        logger.info(f"Column mapping created with {len(column_mapping)} matches")

        # If we don't have the required columns, log an error
        if "case_study_entry" not in column_mapping.values() or "country" not in column_mapping.values():
            logger.error("Required columns 'case_study_entry' and 'country' not found in CSV")

            # Check what columns we did find
            required_cols = ["CaseStudy entry", "Country"]
            found_cols = [
                col for col in df.columns if any(req.lower() in col.lower() for req in required_cols)
            ]
            logger.info(f"Similar columns found: {found_cols}")

            # Try a more direct mapping
            if not column_mapping and len(df.columns) >= 2:
                logger.info("Attempting direct mapping of first two columns")
                column_mapping = {
                    df.columns[0]: "case_study_entry",
                    df.columns[1]: "country",
                }

        # Rename columns to match model fields
        df_renamed = df.rename(columns=column_mapping)

        # Handle missing columns
        for field in CaseStudy.__annotations__:
            if field not in df_renamed.columns:
                logger.debug(f"Adding missing column: {field}")
                df_renamed[field] = None

        # Convert DataFrame to list of CaseStudy objects
        case_studies = []

        # Add error counter for reporting
        error_count = 0

        for _, row in tqdm(df_renamed.iterrows(), total=len(df_renamed), desc="Processing case studies"):
            try:
                # Apply data cleaning and default value handling
                row_dict = row.to_dict()

                # Handle required fields
                if pd.isna(row_dict.get("case_study_entry")) or not row_dict.get("case_study_entry"):
                    row_dict["case_study_entry"] = f"Case Study #{len(case_studies) + 1}"

                if pd.isna(row_dict.get("country")) or not row_dict.get("country"):
                    row_dict["country"] = "Unknown"

                # Handle optional fields - convert NaN to None
                for key, value in row_dict.items():
                    if pd.isna(value):
                        row_dict[key] = None

                # Only include fields defined in the CaseStudy model
                model_fields = {k: v for k, v in row_dict.items() if k in CaseStudy.__annotations__}

                # Log the model fields for the first few rows for debugging
                if len(case_studies) < 3:
                    logger.debug(f"Creating CaseStudy with fields: {model_fields}")

                # Create and append the case study
                case_study = CaseStudy(**model_fields)
                case_studies.append(case_study)

            except Exception as e:
                error_count += 1
                if error_count <= 5:  # Limit log messages to avoid overwhelming log
                    logger.warning(f"Error processing case study: {e}")
                elif error_count == 6:
                    logger.warning("Additional errors encountered but not logged")

        logger.info(f"Loaded {len(case_studies)} case studies, encountered {error_count} errors")
        return case_studies

    except Exception as e:
        logger.error(f"Error loading case studies: {e}")
        import traceback

        logger.error(traceback.format_exc())
        return []


def check_content_uniqueness(case_studies: List[CaseStudy]) -> None:
    """Check if the content for embeddings is unique across case studies.

    Args:
        case_studies: List of CaseStudy objects.
    """
    content_map = {}
    duplicate_count = 0
    very_short_count = 0

    for i, case_study in enumerate(case_studies):
        content = case_study.get_content_for_embedding()

        # Check for very short content
        if len(content) < 100:
            very_short_count += 1
            logger.warning(
                f"Case study with very short content ({len(content)} chars): {case_study.case_study_entry}"
            )

        # Check for duplicates
        if content in content_map:
            duplicate_count += 1
            logger.warning(
                f"Duplicate content detected: {case_study.case_study_entry} has same content as "
                f"{content_map[content]}. Length: {len(content)}"
            )
        else:
            content_map[content] = case_study.case_study_entry

    if duplicate_count > 0:
        logger.warning(
            f"Found {duplicate_count} case studies with duplicate content out of {len(case_studies)}"
        )
    else:
        logger.info(f"All {len(case_studies)} case studies have unique content for embeddings")

    if very_short_count > 0:
        logger.warning(
            f"Found {very_short_count} case studies with very short content (<100 chars)"
        )


def create_documents_from_case_studies(case_studies: List[CaseStudy]) -> List[Document]:
    """Create LlamaIndex documents from case studies.
    
    Args:
        case_studies: List of CaseStudy objects.
        
    Returns:
        List of LlamaIndex Document objects.
    """
    documents = []
    
    for case_study in tqdm(case_studies, desc="Preparing case studies for embedding"):
        # Get text for embedding
        text = case_study.get_content_for_embedding()
        
        # Get metadata (ensuring all fields are strings to avoid issues)
        metadata = {}
        for key, value in case_study.model_dump().items():
            if value is None:
                metadata[key] = ""
            elif isinstance(value, (str, int, float, bool)):
                metadata[key] = value
            else:
                metadata[key] = str(value)
        
        # Create document
        doc = Document(text=text, metadata=metadata)
        documents.append(doc)
    
    return documents


def create_vector_store_index(documents: List[Document]) -> VectorStoreIndex:
    """Create VectorStoreIndex from documents.
    
    Args:
        documents: List of Document objects.
        
    Returns:
        VectorStoreIndex containing the documents.
    """
    logger.info("Creating vector store index")
    
    # Create embedding function
    embed_model = create_embedding_model()
    
    # Create directory for vector database if it doesn't exist
    persist_dir = str(config.vectordb.database_path)
    Path(persist_dir).mkdir(parents=True, exist_ok=True)
    
    # Create Chroma client and collection
    chroma_client = chromadb.PersistentClient(path=persist_dir)
    collection_name = config.vectordb.collection_name
    
    # Try to get collection or create if it doesn't exist
    try:
        collection = chroma_client.get_or_create_collection(collection_name)
    except Exception as e:
        logger.error(f"Error creating Chroma collection: {e}")
        raise
    
    # Create Chroma vector store
    vector_store = ChromaVectorStore(chroma_collection=collection)
    
    # Create storage context
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    
    # Create vector store index
    try:
        # Node parser to split documents (optional)
        parser = SentenceSplitter(chunk_size=1024, chunk_overlap=20)
        nodes = parser.get_nodes_from_documents(documents)
        
        # Add metadata to each node
        for i, node in enumerate(nodes):
            # Keep source document metadata
            if isinstance(node, TextNode) and hasattr(node, 'metadata'):
                doc_idx = min(i // 2, len(documents) - 1)  # Estimate which document this came from
                node.metadata.update(documents[doc_idx].metadata)
                # Add a node_id for reference
                node.id_ = f"node_{i}"
                
        # Log a sample node for debugging
        if nodes:
            logger.debug(f"Sample node text (first 200 chars): {nodes[0].text[:200]}")
            logger.debug(f"Sample node metadata: {nodes[0].metadata}")
        
        # Create index from nodes
        index = VectorStoreIndex(
            nodes=nodes,
            storage_context=storage_context,
            embed_model=embed_model,
        )
        
        logger.info(f"Created vector store index with {len(nodes)} nodes from {len(documents)} documents")
        return index
    
    except Exception as e:
        logger.error(f"Error creating vector store index: {e}")
        import traceback
        logger.error(traceback.format_exc())
        raise


def load_vector_store_index() -> Optional[VectorStoreIndex]:
    """Load existing vector store index.
    
    Returns:
        VectorStoreIndex if it exists, None otherwise.
    """
    db_path = config.vectordb.database_path
    
    if not db_path.exists():
        logger.warning(f"Vector database not found at {db_path}")
        return None
    
    logger.info(f"Loading vector database from {db_path}")
    
    try:
        # Create embedding model
        embed_model = create_embedding_model()
        
        # Create Chroma client
        chroma_client = chromadb.PersistentClient(path=str(db_path))
        collection_name = config.vectordb.collection_name
        
        # Get collection
        try:
            collection = chroma_client.get_collection(collection_name)
            
            # Create vector store
            vector_store = ChromaVectorStore(chroma_collection=collection)
            
            # Create storage context
            storage_context = StorageContext.from_defaults(vector_store=vector_store)
            
            # Create vector store index
            index = VectorStoreIndex.from_vector_store(
                vector_store=vector_store,
                embed_model=embed_model,
            )
            
            # Get document count
            doc_count = len(collection.get(include=[])['ids'])
            logger.info(f"Loaded vector store index with {doc_count} documents")
            
            return index
            
        except Exception as e:
            logger.error(f"Error loading vector store: {e}")
            return None
        
    except Exception as e:
        logger.error(f"Error loading vector store index: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return None


def get_or_create_vector_store_index() -> VectorStoreIndex:
    """Get existing vector store index or create a new one.
    
    Returns:
        VectorStoreIndex.
    """
    # Try to load existing vector store index
    index = load_vector_store_index()
    
    # Create new index if it doesn't exist
    if index is None:
        case_studies = load_case_studies()
        if not case_studies:
            raise ValueError("No case studies loaded. Cannot create vector store index.")
            
        # Check content uniqueness
        check_content_uniqueness(case_studies)
        
        # Create documents from case studies
        documents = create_documents_from_case_studies(case_studies)
        
        # Create index
        index = create_vector_store_index(documents)
    
    return index