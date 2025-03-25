from fastapi import APIRouter, HTTPException, Depends, Body
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import logging

from app.models.advisor import CampaignAdvisor
from app.core.dependencies import get_advisor

router = APIRouter()
logger = logging.getLogger(__name__)

class QueryRequest(BaseModel):
    query: str
    fast_mode: bool = False

class ReferenceItem(BaseModel):
    title: str
    organization: str
    campaign_name: str
    content: str
    id: str

class AdviceResponse(BaseModel):
    query: str
    advice: str
    references: List[ReferenceItem] = Field(default_factory=list)
    model_type: str

@router.post("/ask", response_model=AdviceResponse)
async def get_campaign_advice(
    request: QueryRequest = Body(...),
    advisor: CampaignAdvisor = Depends(get_advisor)
):
    """
    Get AI-powered advice for a GivingTuesday campaign question.
    """
    try:
        logger.info(f"Processing query: {request.query}")
        
        # Get advice from the advisor
        result = advisor.get_advice(
            query=request.query,
            fast_mode=request.fast_mode
        )
        
        return AdviceResponse(
            query=request.query,
            advice=result["advice"],
            references=result.get("references", []),
            model_type="cost-effective" if request.fast_mode else "detailed"
        )
        
    except Exception as e:
        logger.error(f"Error getting advice: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate advice: {str(e)}"
        )