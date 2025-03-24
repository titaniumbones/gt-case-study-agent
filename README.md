# GivingTuesday Campaign Advisor

An AI-powered advisor for planning and executing successful GivingTuesday campaigns, based on real-world case studies.

## Features

- Provides specific, actionable advice based on successful GivingTuesday campaigns
- Analyzes case studies to find relevant examples
- Multi-model architecture:
  - Claude 3.7 Sonnet for high-quality detailed reasoning 
  - Claude 3.5 Haiku for cost-effective quick responses
  - OpenAI Embeddings for efficient vector search
- Query enhancement using cost-effective models
- Supports both command-line and web interfaces
- Designed for easy extension with additional data sources and models

## Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd case-study-agent
   ```

2. Set up the environment using one of these methods:

   ### Using uv (Recommended)
   
   On macOS/Linux:
   ```
   ./setup_env.sh
   source .venv/bin/activate
   ```
   
   On Windows (PowerShell):
   ```
   .\setup_env.ps1
   .\.venv\Scripts\Activate.ps1
   ```

   ### Using standard Python tools
   
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install -e .
   ```

3. Create a `.env` file with your API keys (use `.env.example` as a template):
   ```
   cp .env.example .env
   ```
   
   Then edit the `.env` file to add your API keys and paths:
   - `ANTHROPIC_API_KEY`: Required for Claude models (for reasoning)
   - `OPENAI_API_KEY`: Required for embeddings (for search functionality)
   - `CASE_STUDY_FILE`: Path to the case study CSV file (default: `data/case-study-inventory.csv`)
   
   **Important**: Both API keys must be set for full functionality.

## Usage

### Command Line Interface

Initialize the advisor (first time only):
```
python main.py cli init
```

You can specify a custom case study file:
```
python main.py cli init --case-study-file /path/to/your/case-studies.csv
```

If you need to rebuild the vector database:
```
python main.py cli init --recreate
```

Get advice in interactive mode:
```
python main.py cli ask --interactive
```

Get advice with a specific query:
```
python main.py cli ask "How can I mobilize volunteers for my GivingTuesday campaign?"
```

Use the fast mode with Claude 3.5 Haiku:
```
python main.py cli ask --fast "How can I mobilize volunteers for my GivingTuesday campaign?"
```

Disable query preprocessing:
```
python main.py cli ask --no-preprocessing "How can I mobilize volunteers for my GivingTuesday campaign?"
```

### Developer Search Command

Directly search the vector database to debug and test the embeddings:
```
python main.py search "volunteer mobilization"
```

Show the full content used for embedding:
```
python main.py search "community engagement" --show-content
```

Specify the number of results:
```
python main.py search "fundraising" --top-k=10
```

Format output as JSON:
```
python main.py search "social media" --json
```

Force recreation of the vector database (only if needed):
```
python main.py search "fundraising" --recreate
```

### Web Application

Start the web server:
```
python main.py web
```

Then open http://127.0.0.1:8001 in your browser.

## Project Structure

- `src/`: Main source code
  - `data/`: Data loading and processing
  - `models/`: AI models and advisor logic
  - `utils/`: Utility functions
  - `cli/`: Command-line interface
  - `web/`: Web application
- `data/`: Data files
  - `case-study-inventory.csv`: GivingTuesday case studies
- `tests/`: Unit tests

## Development

Run tests:
```
pytest
```

Format code:
```
black .
isort .
```

Type checking:
```
mypy src
```

Compile SCSS to CSS:
```
python build_css.py
```
*Note: You must run this whenever you modify SCSS files*

## Using uv for Package Management

uv offers significant performance improvements over traditional pip:

- Install a package:
  ```
  uv pip install <package-name>
  ```
  
- Install from requirements.txt:
  ```
  uv pip install -r requirements.txt
  ```
  
- Update a package:
  ```
  uv pip install -U <package-name>
  ```

- Install langchain-anthropic (if missing):
  ```
  uv pip install langchain-anthropic
  ```

## License

[MIT License](LICENSE)