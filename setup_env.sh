#!/bin/bash
# Setup script for creating and configuring a virtual environment using uv

# Exit on error
set -e

# Color output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Create .venv directory if it doesn't exist
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}Creating virtual environment with uv...${NC}"
    uv venv .venv
else
    echo -e "${YELLOW}Virtual environment already exists.${NC}"
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source .venv/bin/activate

# Install dependencies with uv
echo -e "${YELLOW}Installing dependencies with uv...${NC}"
uv pip install -r requirements.txt

# Install the package in development mode
echo -e "${YELLOW}Installing package in development mode...${NC}"
uv pip install -e .

# Display success message
echo -e "${GREEN}Setup complete! Virtual environment is ready.${NC}"
echo -e "${GREEN}To activate the environment, run:${NC}"
echo -e "source .venv/bin/activate"