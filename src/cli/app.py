"""Command line interface for the GivingTuesday Campaign Advisor."""

import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from src.data.loader import get_or_create_vector_store_index
from src.models.advisor import CampaignAdvisor
from src.utils.logging import logger, setup_logging

# Create Typer app
app = typer.Typer(
    name="gt-campaign-advisor",
    help="GivingTuesday Campaign Advisor CLI",
    add_completion=False,
)

# Create console for rich output
console = Console()


@app.command()
def init(
    case_study_file: Optional[Path] = typer.Option(
        None,
        "--case-study-file",
        "-f",
        help="Path to case study CSV file",
    ),
    recreate: bool = typer.Option(
        False,
        "--recreate",
        "-r",
        help="Recreate vector database even if it already exists",
    ),
):
    """Initialize the GivingTuesday Campaign Advisor."""
    # Set up logging
    setup_logging(level="INFO")

    try:
        # If recreate is True, delete the existing vector database
        if recreate:
            from src.utils.config import config
            import shutil

            db_path = config.vectordb.database_path
            if db_path.exists():
                logger.info(f"Deleting existing vector database at {db_path}")
                shutil.rmtree(db_path)

        # First check if the required API keys are set
        from src.utils.config import config

        if not config.models.openai_api_key:
            console.print("[bold red]Error: OpenAI API key not set.[/bold red]")
            console.print(
                "You must set the OPENAI_API_KEY in your .env file for embeddings to work."
            )
            console.print("This is required for the vector database to function.")
            console.print("")
            console.print(
                "Please create or edit your .env file and add the following line:"
            )
            console.print("OPENAI_API_KEY=your_api_key_here")
            console.print("")
            console.print(
                "You can get an API key from https://platform.openai.com/api-keys"
            )

            # Exit with error
            sys.exit(1)

        # For initialization, we should explicitly create the vector store index
        # rather than try to load an existing one that might be empty
        from src.data.loader import (
            load_case_studies,
            create_documents_from_case_studies,
            create_vector_store_index,
            load_vector_store_index,
        )

        # First try to load existing vector store index
        index = load_vector_store_index()
        try:
            # Check if the index is empty
            doc_count = 0
            if index is not None:
                vector_store = index._vector_store
                if hasattr(vector_store, "get"):
                    doc_count = len(vector_store.get(include=[])["ids"])
        except Exception as e:
            logger.debug(f"Error checking vector store document count: {e}")
            doc_count = 0
            
        if index is None or doc_count == 0:
            # If index doesn't exist or is empty, create new one
            logger.info("Creating new vector store index with case studies")

            if not config.models.openai_api_key:
                console.print(
                    "[bold red]Error: Cannot create embeddings without OpenAI API key.[/bold red]"
                )
                console.print(
                    "Please set the OPENAI_API_KEY in your .env file and try again."
                )
                sys.exit(1)

            # If case_study_file is provided, use it; otherwise use the default path
            if case_study_file:
                logger.info(f"Using provided case study file: {case_study_file}")

                # Ensure the file exists
                if not case_study_file.exists():
                    raise ValueError(f"Case study file not found: {case_study_file}")

                case_studies = load_case_studies(case_study_file)
            else:
                # Use the default path, but ensure it's absolute
                from src.utils.config import config

                default_path = Path(config.case_study_file)

                # Convert to absolute path if needed
                if not default_path.is_absolute():
                    default_path = Path.cwd() / default_path

                logger.info(f"Using default case study file: {default_path}")
                case_studies = load_case_studies(default_path)

            if not case_studies:
                raise ValueError("No case studies loaded. Please check the file path.")

            logger.info(f"Loaded {len(case_studies)} case studies, creating documents")
            documents = create_documents_from_case_studies(case_studies)
            
            logger.info(f"Creating vector store index with {len(documents)} documents")
            index = create_vector_store_index(documents)
        
        # Try to get document count for summary
        try:
            vector_store = index._vector_store
            if hasattr(vector_store, "get"):
                doc_count = len(vector_store.get(include=[])["ids"])
            else:
                doc_count = "Unknown"
        except Exception as e:
            logger.debug(f"Error getting document count: {e}")
            doc_count = "Unknown"

        console.print(
            Panel(
                f"[bold green]GivingTuesday Campaign Advisor initialized successfully![/bold green]\n"
                f"Vector store index contains {doc_count} documents."
            )
        )

    except Exception as e:
        logger.error(f"Error initializing advisor: {e}")
        console.print(f"[bold red]Error initializing advisor:[/bold red] {e}")
        sys.exit(1)


@app.command()
def search(
    query: str = typer.Argument(
        ...,  # Required
        help="Direct search query for the vector database",
    ),
    top_k: int = typer.Option(
        5,
        "--top-k",
        "-k",
        help="Number of results to return",
    ),
    show_content: bool = typer.Option(
        False,
        "--show-content",
        "-c",
        help="Show the full content used for embedding",
    ),
    format_json: bool = typer.Option(
        False,
        "--json",
        "-j",
        help="Format output as JSON",
    ),
    recreate: bool = typer.Option(
        False,
        "--recreate",
        "-r",
        help="Recreate vector database even if it already exists",
    ),
):
    """Developer tool to directly search the vector database."""
    # Set up logging
    setup_logging(level="INFO")

    try:
        if recreate:
            # If recreate is True, delete the existing vector database
            from src.utils.config import config
            import shutil

            db_path = config.vectordb.database_path
            if db_path.exists():
                logger.info(f"Deleting existing vector database at {db_path}")
                shutil.rmtree(db_path)

        # Get or create vector store index - will only create if needed
        index = get_or_create_vector_store_index()

        # Show stats about the vector store index
        try:
            vector_store = index._vector_store
            count = len(vector_store.get(include=[])["ids"]) if hasattr(vector_store, "get") else "Unknown"
            console.print(
                f"Using vector store index with [bold cyan]{count}[/bold cyan] documents"
            )
        except Exception as e:
            logger.debug(f"Could not get vector store document count: {e}")

        # Create retriever to perform direct search
        from llama_index.core.retrievers import VectorIndexRetriever
        retriever = VectorIndexRetriever(
            index=index,
            similarity_top_k=top_k,
        )
        nodes = retriever.retrieve(query)

        if format_json:
            import json

            output = []
            for i, node in enumerate(nodes, 1):
                score = round(node.score, 4) if hasattr(node, 'score') else "N/A"
                item = {
                    "rank": i,
                    "title": node.metadata.get("case_study_entry", "Unknown"),
                    "country": node.metadata.get("country", "Unknown"),
                    "score": score
                }

                if show_content:
                    item["content"] = node.text

                output.append(item)

            console.print(json.dumps(output, indent=2))
        else:
            # Display results in human-readable format
            console.print(Panel(f"[bold]Search Results for:[/bold] {query}"))

            for i, node in enumerate(nodes, 1):
                title = node.metadata.get("case_study_entry", "Unknown Case Study")
                country = node.metadata.get("country", "Unknown")
                score = round(node.score, 4) if hasattr(node, 'score') else "N/A"

                console.print(f"\n[bold cyan]{i}. {title}[/bold cyan] ({country}) [Score: {score}]")

                # Show metadata highlights
                if node.metadata.get("focus_area"):
                    console.print(
                        f"[bold]Focus Area:[/bold] {node.metadata['focus_area']}"
                    )

                if node.metadata.get("main_theme"):
                    console.print(f"[bold]Theme:[/bold] {node.metadata['main_theme']}")

                # Show content if requested
                if show_content:
                    console.print("\n[bold]Content used for embedding:[/bold]")
                    console.print(node.text)
                    console.print("---")

    except Exception as e:
        logger.error(f"Error searching vector store: {e}")
        console.print(f"[bold red]Error searching vector store:[/bold red] {e}")
        sys.exit(1)


@app.command()
def ask(
    query: Optional[str] = typer.Argument(
        None,
        help="Query for campaign advice",
    ),
    interactive: bool = typer.Option(
        False,
        "--interactive",
        "-i",
        help="Interactive mode",
    ),
    fast_mode: bool = typer.Option(
        False,
        "--fast",
        "-f",
        help="Use cost-effective model for advice (faster but less detailed)",
    ),
    no_preprocessing: bool = typer.Option(
        False,
        "--no-preprocessing",
        help="Disable query preprocessing",
    ),
):
    """Get advice for a GivingTuesday campaign."""
    # Set up logging
    setup_logging(level="INFO")

    try:
        # Get or create vector store index
        index = get_or_create_vector_store_index()

        # Create appropriate model
        if fast_mode:
            from src.models.factory import create_cost_effective_model

            model = create_cost_effective_model()
            logger.info("Using cost-effective model for advice generation")
        else:
            from src.models.factory import create_reasoning_model

            model = create_reasoning_model()
            logger.info("Using high-quality reasoning model for advice generation")

        # Create campaign advisor
        advisor = CampaignAdvisor(
            index, model=model, use_query_enhancement=not no_preprocessing
        )

        if interactive:
            # Interactive mode
            console.print(
                Panel(
                    "[bold]GivingTuesday Campaign Advisor[/bold]\n"
                    "Ask questions about how to plan and execute your GivingTuesday campaign.\n"
                    "Type 'exit' or 'quit' to exit."
                )
            )

            while True:
                # Get query from user
                query = console.input(
                    "\n[bold cyan]How can I help with your campaign?[/bold cyan] "
                )

                # Exit if requested
                if query.lower() in ("exit", "quit"):
                    break

                # Skip empty queries
                if not query.strip():
                    continue

                # Generate advice
                with console.status("[bold green]Generating advice...[/bold green]"):
                    advice = advisor.get_advice(query)

                # Display advice
                console.print(Markdown(advice.advice))

                # Display references
                if advice.references:
                    console.print("\n[bold]References:[/bold]")
                    for ref in advice.references:
                        console.print(f"- {ref}")

        else:
            # Command line mode
            if not query:
                console.print(
                    "[bold red]Please provide a query or use interactive mode.[/bold red]"
                )
                sys.exit(1)

            # Generate advice
            with console.status("[bold green]Generating advice...[/bold green]"):
                advice = advisor.get_advice(query)

            # Display advice
            console.print(Markdown(advice.advice))

            # Display references
            if advice.references:
                console.print("\n[bold]References:[/bold]")
                for ref in advice.references:
                    console.print(f"- {ref}")

    except Exception as e:
        logger.error(f"Error getting advice: {e}")
        console.print(f"[bold red]Error getting advice:[/bold red] {e}")
        sys.exit(1)


def main():
    """Run the CLI application."""
    app()
