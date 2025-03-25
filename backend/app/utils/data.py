import csv
import logging
from pathlib import Path
from typing import List, Dict, Optional

from llama_index.core import Document

logger = logging.getLogger(__name__)

def load_case_studies_from_csv(csv_path: str) -> List[Document]:
    """
    Load case studies from a CSV file and convert them to LlamaIndex documents.
    
    Args:
        csv_path: Path to the CSV file
        
    Returns:
        List of Document objects
    """
    csv_path = Path(csv_path)
    
    if not csv_path.exists():
        logger.error(f"CSV file not found: {csv_path}")
        return []
    
    documents = []
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for i, row in enumerate(reader):
                # Extract fields with better fallbacks
                org_name = row.get('Lead/institution Name', '').strip() or row.get('Country', '').strip()
                
                # Try to get a meaningful campaign name
                campaign_name = None
                for field in ['CaseStudy entry', 'Focus Area/ Cause/participating category', 'Main Theme']:
                    if field in row and row[field] and len(row[field].strip()) > 0:
                        campaign_name = row[field].strip()
                        break
                
                if not campaign_name:
                    campaign_name = f"Case Study #{i+1}"
                
                # Get detailed content
                description = row.get('Full story', '') or row.get('Goals (What are they trying to do)', '')
                strategies = row.get('Key Activities', '')
                results = row.get('Outcomes/ Results (if applicable)', '')
                themes = []
                
                # Add themes if available
                for field in ['Main Theme', 'Subtheme', 'GT related themes/subthemes']:
                    if field in row and row[field] and len(row[field].strip()) > 0:
                        themes.append(f"{field}: {row[field].strip()}")
                
                # Build document text
                doc_text = f"# {org_name}: {campaign_name}\n\n"
                
                if description:
                    doc_text += f"## Description\n{description}\n\n"
                    
                if strategies:
                    doc_text += f"## Strategies\n{strategies}\n\n"
                    
                if results:
                    doc_text += f"## Results\n{results}\n\n"
                
                if themes:
                    doc_text += f"## Themes\n" + "\n".join(themes) + "\n\n"
                
                # Create metadata
                metadata = {
                    "organization": org_name if org_name else "GivingTuesday Organization",
                    "campaign_name": campaign_name,
                    "source": str(csv_path),
                }
                
                # Create document
                document = Document(
                    text=doc_text,
                    metadata=metadata
                )
                
                documents.append(document)
        
        logger.info(f"Loaded {len(documents)} case studies from {csv_path}")
        return documents
        
    except Exception as e:
        logger.error(f"Error loading case studies from CSV: {str(e)}")
        return []