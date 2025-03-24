# Deployment Guide

This document outlines deployment options for the GivingTuesday Campaign Advisor application.

## Deployment Requirements

The GivingTuesday Campaign Advisor requires a server environment capable of:
- Running Python 3.9+
- Storing files persistently (for the vector database)
- Managing API keys securely
- Processing HTTP requests via FastAPI

## Hosting Limitations

### Static Hosting Platforms (GitHub Pages, Netlify Static, etc.)

This application cannot be deployed directly to static hosting platforms due to:

1. **Server-side Processing Requirements**
   - Python code execution for data processing and AI model interaction
   - Vector database operations via ChromaDB
   - Form handling with FastAPI

2. **API Key Security**
   - Secure management of OpenAI and Anthropic API keys
   - Protection of credentials from client-side exposure

3. **Persistence Requirements**
   - Vector store database must persist between requests
   - File system access for data storage

## Recommended Deployment Options

### Option 1: Single-Server Deployment (Recommended for Production)

Deploy on a VPS or cloud instance:
```
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
export OPENAI_API_KEY="your-openai-key"
export ANTHROPIC_API_KEY="your-anthropic-key"

# Run the application with a production ASGI server
uvicorn src.web.app:app --host 0.0.0.0 --port 8001
```

For production, consider:
- Using Gunicorn as a process manager with Uvicorn workers
- Setting up Nginx as a reverse proxy
- Implementing HTTPS with Let's Encrypt
- Using environment variables or .env files (with proper permissions)

### Option 2: Platform-as-a-Service (Simpler Deployment)

Deploy to Heroku, Render, or similar platforms:
1. Configure the platform to use Python 3.9+
2. Set environment variables for API keys
3. Ensure the platform supports persistent storage (for ChromaDB)

Example for Heroku:
```bash
# Add a Procfile
echo "web: uvicorn src.web.app:app --host 0.0.0.0 --port \$PORT" > Procfile

# Deploy
git push heroku main

# Set environment variables
heroku config:set OPENAI_API_KEY="your-openai-key"
heroku config:set ANTHROPIC_API_KEY="your-anthropic-key"
```

## Alternative Architectures

If you need to use static hosting, significant architectural changes would be required:

### Split Architecture
- Develop a separate backend API service hosted on a server
- Convert the frontend to a static site making requests to your API
- Host only the frontend on GitHub Pages

### Serverless Approach
- Implement key functionality as serverless functions (AWS Lambda, Netlify Functions)
- Create a lightweight frontend that calls these functions
- Host the frontend on a static hosting service

## Development Server

For local development:
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables (or use .env file)
export OPENAI_API_KEY="your-openai-key"
export ANTHROPIC_API_KEY="your-anthropic-key"

# Run the development server
python main.py web
```

This will start the application on http://127.0.0.1:8001.

## Database Considerations

- The vector database (ChromaDB) requires persistent storage
- Ensure your deployment environment has sufficient disk space
- Consider performance implications of disk I/O for production environments
- Backup the `vectordb` directory regularly in production environments

## Security Considerations

- Never commit API keys to version control
- Set restrictive permissions on .env files
- Consider API key rotation schedules
- Implement rate limiting for production deployments