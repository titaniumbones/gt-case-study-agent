"""Web application for the GivingTuesday Campaign Advisor."""

from fastapi import Depends, FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from src.data.loader import get_or_create_vector_store_index
from src.data.schema import CampaignAdvice, CampaignQuery
from src.models.advisor import CampaignAdvisor
from src.utils.logging import logger, setup_logging
from src.utils.markdown import markdown_to_html

# Set up logging
setup_logging(level="INFO")

# Create FastAPI app
app = FastAPI(
    title="GivingTuesday Campaign Advisor",
    description="Get advice for your GivingTuesday campaign based on successful case studies.",
    version="0.1.0",
)

# Set up templates
templates = Jinja2Templates(directory="src/web/templates")

# Mount static files directory
app.mount("/static", StaticFiles(directory="src/web/static"), name="static")

# Create campaign advisor
@app.on_event("startup")
async def startup_event():
    # Get or create vector store index
    index = get_or_create_vector_store_index()
    
    # Create models
    from src.models.factory import create_reasoning_model, create_cost_effective_model
    
    # Create high-quality advisor
    app.state.high_quality_advisor = CampaignAdvisor(
        index,
        model=create_reasoning_model(),
        use_query_enhancement=True
    )
    
    # Create cost-effective advisor
    app.state.cost_effective_advisor = CampaignAdvisor(
        index,
        model=create_cost_effective_model(),
        use_query_enhancement=True
    )
    
    # Default advisor
    app.state.advisor = app.state.high_quality_advisor
    
    # Try to log document count
    try:
        # First try to get node count if available
        nodes = index._nodes if hasattr(index, "_nodes") else []
        if nodes:
            doc_count = len(nodes)
        else:
            # If nodes not available, try to get from vector store
            vector_store = index._vector_store
            if hasattr(vector_store, "get"):
                # For ChromaVectorStore, use get() method
                doc_count = len(vector_store.get(include=[])["ids"])
            elif hasattr(vector_store, "_collection"):
                # For older versions, try the collection
                doc_count = vector_store._collection.count()
            else:
                doc_count = "Unknown"
        
        logger.info(f"Vector store index loaded with {doc_count} documents")
    except Exception as e:
        logger.debug(f"Could not get document count: {e}")
    
    logger.info("Web application started")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Render the index page."""
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "title": "GivingTuesday Campaign Advisor"}
    )


@app.post("/api/advice", response_model=CampaignAdvice)
async def get_advice(query: CampaignQuery, fast: bool = False):
    """Get advice for a GivingTuesday campaign."""
    # Select advisor based on fast parameter
    advisor = app.state.cost_effective_advisor if fast else app.state.high_quality_advisor
    
    # Generate advice
    advice = advisor.get_advice(query.query)
    
    return advice


@app.post("/ask", response_class=HTMLResponse)
async def ask(request: Request, query: str = Form(...), fast_mode: bool = Form(False)):
    """Handle form submission and render the results page."""
    # Select advisor based on fast_mode parameter
    advisor = app.state.cost_effective_advisor if fast_mode else app.state.high_quality_advisor
    
    # Log which model is being used
    model_type = "cost-effective" if fast_mode else "high-quality"
    logger.info(f"Using {model_type} model for advice generation")
    
    # Generate advice
    advice = advisor.get_advice(query)
    
    # Convert markdown to HTML
    html_advice = markdown_to_html(advice.advice)
    
    return templates.TemplateResponse(
        "results.html",
        {
            "request": request,
            "title": "GivingTuesday Campaign Advisor",
            "query": query,
            "advice": html_advice,
            "references": advice.references,
            "model_type": model_type
        }
    )