# PMID PDF API

A Flask-based API for retrieving PDF full text links based on PMID (PubMed ID).

## Features

- Retrieve PDF links from local database by PMID
- Download PDFs using metapub package if not found locally
- API validation using spectree
- MySQL database with SQLAlchemy ORM
- Docker containerization
- Authentication implementation
- Error handling with custom codes and messages
- MCP (Model Context Protocol) compliance for future LLM integration

## Setup and Installation

### Prerequisites

- Python 3.9+
- Docker
- MySQL

### Running with Docker

1. Clone the repository
2. Configure your environment variables in a `.env` file
3. Build and run the Docker container:

```bash
docker build -t pmid-pdf-api .
docker run -p 8091:8091 -v /Users/jiaoyk/Downloads:/app/downloads --env-file .env pmid-pdf-api
```

## API Documentation

The API documentation is available through both Swagger UI and ReDoc interfaces when the service is running:

- **Swagger UI**: `http://${SERVER_ADDRESS}:${PORT}/apidoc/swagger/`
  - Interactive documentation that allows you to test API endpoints directly from the browser

- **ReDoc**: `http://${SERVER_ADDRESS}:${PORT}/apidoc/redoc/`
  - Clean, responsive documentation with a three-panel design

These documentation interfaces provide:
- Detailed information about all available endpoints
- Request and response schemas
- Authentication requirements
- Example requests and responses

For example, if running locally with default port 8091:
- Swagger UI: http://localhost:8091/apidoc/swagger/
- ReDoc: http://localhost:8091/apidoc/redoc/
