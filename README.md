# GivingTuesday Campaign Advisor

An AI-powered advisor for planning and executing successful GivingTuesday campaigns, based on real-world case studies.

## Features

- Provides specific, actionable advice based on successful GivingTuesday campaigns
- Analyzes case studies to find relevant examples
- Multi-model architecture using LlamaIndex:
  - Claude 3.7 Sonnet for high-quality detailed reasoning 
  - Claude 3.5 Haiku for cost-effective quick responses
  - OpenAI Embeddings for efficient vector search
- Query enhancement using cost-effective models
- Modern React frontend with Material UI components
- FastAPI backend for efficient API handling
- Designed for easy extension with additional data sources and models
- Built with modern LlamaIndex retrieval techniques

## Project Structure

This project uses a modern architecture with a React frontend and FastAPI backend:

- `frontend/`: React application built with Material UI
- `backend/`: FastAPI application with LlamaIndex integration
- `data/`: Data files including case study CSV

## Installation

### Backend

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

   If you encounter any issues with LlamaIndex dependencies, you can try installing them individually:
   ```
   pip install fastapi uvicorn pydantic pydantic-settings python-dotenv
   pip install llama-index-core llama-index-llms-anthropic llama-index-embeddings-openai llama-index-vector-stores-chroma
   pip install chromadb markdown bleach
   ```

4. Create a `.env` file from the example:
   ```
   cp .env.example .env
   ```
   
   Edit the `.env` file to add your API keys:
   - `ANTHROPIC_API_KEY`: Required for Claude models
   - `OPENAI_API_KEY`: Required for embeddings

### Frontend

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

## Running the Application

### Development Mode

1. Start the backend server:
   ```
   cd backend
   python run.py --reload
   ```

2. In a new terminal, start the frontend development server:
   ```
   cd frontend
   npm start
   ```
   
   If you encounter any host check issues, you can run:
   ```
   DANGEROUSLY_DISABLE_HOST_CHECK=true npm start
   ```
   
   For Windows PowerShell:
   ```
   $env:DANGEROUSLY_DISABLE_HOST_CHECK="true"; npm start
   ```

3. Visit `http://localhost:3000` in your browser.

### Troubleshooting

#### WebSocket Connection Error
If you see errors about WebSocket connections, this is typically just a warning and won't affect the application's functionality. The frontend and backend communicate via HTTP, not WebSockets.

#### CORS Error
If you encounter CORS issues, make sure both servers are running and check the console for specific error messages. The backend has been configured to accept requests from any origin during development.

#### API Connection Error
If the frontend can't connect to the backend API, verify:
- The backend server is running on port 8001
- There are no firewall issues blocking local connections
- The API endpoints match what the frontend expects (http://localhost:8001/api)

#### Pydantic Error
If you encounter errors related to Pydantic or BaseSettings:
```
pip install pydantic==1.10.7  # Use older version if needed
# OR
pip install pydantic-settings  # For newer pydantic
```

### Production Mode

For production deployment:

1. Build the frontend:
   ```
   cd frontend
   npm run build
   ```

2. Run the backend server:
   ```
   cd backend
   python run.py --host 0.0.0.0 --port 8001
   ```

3. The application will be available at `http://your-server-ip:8001`.

## API Documentation

When the backend is running, API documentation is available at:
- Swagger UI: `http://localhost:8001/docs`
- ReDoc: `http://localhost:8001/redoc`

## License

[MIT License](LICENSE)