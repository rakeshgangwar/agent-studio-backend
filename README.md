# Agent Studio Backend

## Status
This project is a Work In Progress (WIP). Currently, we are working on setting up the basic structure and functionality of the backend. Future plans include adding more features and improving the existing ones.

## Project Description
Agent Studio Backend is a FastAPI-based backend service for managing AI agents. It provides endpoints for creating, updating, and deleting agents, as well as executing them. The backend integrates with various AI models and tools to provide a comprehensive solution for AI agent management.

## Installation Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/rakeshgangwar/agent-studio-backend.git
   cd agent-studio-backend
   ```

2. Install dependencies:
   ```bash
   poetry install
   ```

## Configuration Instructions
1. Copy the example environment file and update it with your configuration:
   ```bash
   cp .env.example .env.local
   ```

2. Open the `.env.local` file and set the required environment variables:
   ```env
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   OPENAI_API_KEY=your_openai_api_key
   TAVILY_API_KEY=your_tavily_api_key
   OPENWEATHER_APPID=your_openweather_appid
   ANTHROPIC_API_KEY=your_anthropic_api_key
   ```

## Usage Instructions
1. Run the FastAPI server:
   ```bash
   poetry run uvicorn app.main:app --reload
   ```

2. Open your browser and navigate to `http://localhost:8000` to see the API documentation.

## Main Features and Endpoints
- **Agents**: Create, update, delete, and list AI agents.
- **Models**: Manage AI models and their providers.
- **Prompts**: Create, update, delete, and list prompts for AI agents.
- **Tools**: Integrate various tools for AI agents to use.

## Dependencies
- Python 3.10
- FastAPI
- Uvicorn
- Langchain-OpenAI
- Langchain
- Supabase
- Langchain-Anthropic
- Langgraph
- Langchain-Community
- Python-Dotenv
- BeautifulSoup4
- Langchain-Ollama

## Contact Information
For any questions or support, please contact the project maintainer:
- Name: Rakesh Gangwar
- Email: rakesh@superjackfruit.com
