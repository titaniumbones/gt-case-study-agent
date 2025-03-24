# Claude Agent Instructions

## Project Description
We are building a LlamaIndex-based RAG application that gives advice on building GivingTuesday campaigns. Advice comes from descriptions of successful GivingTuesday campaigns listed in `data/case-study-inventory.csv`. The project uses a mix of inexpensive AIs for initial processing, and expensive reasoning models. The system is designed to allow adding additional datasources when they become available.

The application was originally built with LangChain but has been migrated to LlamaIndex for improved retrieval capabilities and better maintainability.

## Build Commands
- Setup with uv (recommended): `./setup_env.sh` or `.\setup_env.ps1` on Windows
- Install dependencies: `uv pip install -r requirements.txt` 
- Install in development mode: `uv pip install -e .`
- Alternative (standard pip): `pip install -r requirements.txt && pip install -e .`

## Lint and Formatting
- Format code: `black .`
- Sort imports: `isort .`
- Type checking: `mypy src`
- Linting: `ruff check src`
- Build assets: `python build_css.py`

## Test Commands
- Run all tests: `pytest`
- Run single test: `pytest tests/test_file.py::test_function`
- Run tests with verbosity: `pytest -v`

## Run Commands
- CLI initialization: `python main.py cli init`
- CLI query: `python main.py cli ask "How can I mobilize volunteers?"`
- CLI interactive: `python main.py cli ask --interactive`
- Web application: `python main.py web`
- Developer search: `python main.py search "volunteer mobilization" --show-content`

## Asset Building
- Compile SCSS to CSS: `python build_css.py`
  - Must run this whenever SCSS files are modified
  - Creates compiled CSS files in src/web/static/css/ directory

## Code Style Guidelines
- Follow PEP 8 for Python code
- Use type hints for all function parameters and return values
- Group imports: standard library, third-party, local 
- Document classes and functions with docstrings
- Use descriptive variable names in snake_case
- Error handling: Use try/except blocks with specific exceptions
- Use f-strings for string formatting
- Use Path objects from pathlib for file operations
- Follow LlamaIndex conventions for model and index definitions

## Project Structure
- Data processing in `src/data/`
- AI models in `src/models/`
- CLI interface in `src/cli/`
- Web interface in `src/web/`
- Config and utilities in `src/utils/`
- Tests in `tests/`

## Environment Management
- Use uv for fast package management
- Virtual environment is in `.venv/` directory
- Activate with `source .venv/bin/activate` (Unix) or `.\.venv\Scripts\Activate.ps1` (Windows)
- If LlamaIndex packages are missing: `uv pip install llama-index-llms-anthropic llama-index-embeddings-openai`
- For web interface with markdown support: `uv pip install markdown bleach`

## Key LlamaIndex Components
- `VectorStoreIndex`: Main index for storing and searching case studies
- `ChromaVectorStore`: Persistent vector store backend
- `TextNode`: Storage unit for text chunks with metadata
- `VectorIndexRetriever`: Retriever for finding relevant nodes
- `SentenceSplitter`: Text chunking strategy
- `Anthropic` and `OpenAI` classes for LLM and embedding models