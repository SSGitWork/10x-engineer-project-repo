# PromptLab

PromptLab is a developer-focused tool for storing, organizing, tagging, and testing AI prompts in structured collections.

It provides a lightweight REST API built with **FastAPI** and a user-friendly frontend built with **React** to allow AI engineers to manage prompt libraries, experiment with prompt variations, and collaborate efficiently.

---

# Table of Contents

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation Guide](#installation-guide)
- [Running the Backend](#running-the-backend)
- [Running the Frontend](#running-the-frontend)
- [Docker Usage](#docker-usage)
- [API Summary](#api-summary)
- [Usage Examples](#usage-examples)
- [Testing](#testing)
- [CI Integration](#ci-integration)
- [Contribution Guide](#contribution-guide)
- [License](#license)

---

# Project Overview

PromptLab is designed to simplify prompt management workflows for AI development.

It enables teams to:

- Store prompts in reusable collections
- Organize prompts using tags
- Update and maintain prompt versions easily
- Access prompts through a REST API and a web frontend
- Collaborate on prompt engineering workflows

The project currently uses **in-memory storage** but is designed to support future database integrations.

---

# Architecture

PromptLab follows a modular architecture separating frontend and backend components.

```
PromptLab/
├── backend/
│   ├── app/
│   │   ├── api.py           # FastAPI route definitions
│   │   ├── models.py        # Pydantic models/schemas
│   │   ├── storage.py       # In-memory storage and business logic
│   │   ├── utils.py         # Shared helpers and utilities
│   │   
│   │
│   ├── tests/
│   │   ├── test_api_prompts.py
│   │   ├── test_api_collections.py
│   │   └── test_tagging.py
|   |
|   ├── Dockerfile               # Docker container configuration
|   ├── requirements.txt
│   └── main.py          # FastAPI application entry point
|   
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── App.tsx          # Main entry point for React
│   │   └── main.tsx         # ReactDOM render setup
│   │
│   ├── public/              # Static files and index.html
│   └── package.json         # Frontend dependencies and scripts
│
├── .github/
│   └── workflows/
│       └── ci.yml           # GitHub Actions CI pipeline
│
├── docker-compose.yml       # Local container orchestration
└── README.md
```

### Core Components

**backend/app/api.py**

Defines FastAPI routes for managing prompts, collections, and tags.

**backend/app/models.py**

Contains Pydantic models used for request validation and response schemas.

**backend/app/storage.py**

Implements in-memory storage logic for prompts, collections, and tags.

**frontend/src/components**

Contains React components for the UI.

---

# Prerequisites

Before running PromptLab ensure the following tools are installed:

- Python **3.11+**
- Node.js **14.0+** and npm (for frontend development)
- pip (Python package installer)
- Git **2.40+**
- Docker (optional, for containerized execution)

--- 

# Installation Guide

### 1. Clone the Repository

```shell
git clone <repository-url>
cd PromptLab
```

### 2. Navigate to Backend

```shell
cd backend
```

### 3. Create a Virtual Environment

```shell
python -m venv venv
```

### 4. Activate the Virtual Environment

Windows

```shell
venv\Scripts\activate
```

macOS / Linux

```shell
source venv/bin/activate
```

### 5. Install Dependencies

```shell
pip install -r requirements.txt
```

--- 

# Running the Backend

Start the FastAPI development server.

```shell
cd backend
uvicorn main:app --reload
```

The application will be available at:

```
http://127.0.0.1:8000
```

Interactive API documentation:

```
http://127.0.0.1:8000/docs
```

--- 

# Running the Frontend

Navigate to the `frontend` directory and install dependencies:

```shell
cd frontend
npm install
```

Start the React development server:

```shell
npm start
```

The frontend application will be accessible at:

```
http://localhost:3000
```

--- 

# Docker Usage

PromptLab can also be run using Docker for easier local deployment and testing.

## Build the Docker Image

From the project root directory:

```shell
docker-compose up --build
```

This will:

- Build container images for both the backend and frontend
- Start PromptLab services
- Expose the API on port **8000** and frontend on port **3000**

--- 

## Using Docker Compose

Docker Compose simplifies local deployment.

Start the application:

```shell
docker-compose up --build
```

Stop the application:

```shell
docker-compose down
```

This will:

- Build the container image
- Start the PromptLab backend service
- Expose the API on port **8000**

---

# API Summary

PromptLab exposes RESTful endpoints for managing **prompts**, **collections**, and system health checks.

For complete request/response examples and detailed documentation, see:

```
docs/API_REFERENCE.md
```

---

## Health

- `GET /health`  
  Returns the health status and current API version.

---

## Prompts

- `GET /prompts`  
  List prompts with optional filtering.

  Optional query parameters:
  - `collection_id` — Filter prompts by collection
  - `search` — Search prompts by title or content
  - `tags` — Comma-separated list of tags

- `GET /prompts/{prompt_id}`  
  Retrieve a specific prompt by ID.

- `POST /prompts`  
  Create a new prompt.

- `PUT /prompts/{prompt_id}`  
  Replace all fields of an existing prompt.

- `PATCH /prompts/{prompt_id}`  
  Partially update fields of an existing prompt.

- `DELETE /prompts/{prompt_id}`  
  Delete a prompt by ID.

---

## Collections

- `GET /collections`  
  List all collections.

- `GET /collections/{collection_id}`  
  Retrieve a specific collection.

- `POST /collections`  
  Create a new collection.

- `DELETE /collections/{collection_id}`  
  Delete a collection and its associated prompts.

---

## Error Responses

Errors follow a consistent JSON structure.

Example:

```json
{
  "detail": "Prompt not found"
}
```

Common status codes:

- **400** – Invalid input or business rule violation
- **404** – Resource not found
- **422** – Validation error
- **500** – Unexpected server error

---

# Usage Examples

## Create a Collection

Request:

```
POST /collections
```

Body:

```json
{
  "name": "Customer Support Prompts",
  "description": "Prompts used for customer support workflows"
}
```

---

## Create a Prompt

Request:

```
POST /prompts
```

Body:

```json
{
  "name": "Greeting Prompt",
  "content": "Hello {{customer_name}}, how can I help you today?",
  "collection_id": "col-123",
  "tags": ["greeting", "support"]
}
```

---

## Retrieve a Prompt

```
GET /prompts/{prompt_id}
```

Example:

```
GET /prompts/prm-abc123
```

---

## List All Prompts

```
GET /prompts
```

---

## Delete a Prompt

```
DELETE /prompts/{prompt_id}
```

---

# Testing

PromptLab uses **pytest** for automated testing.

Run the test suite:

```shell
cd backend
pytest tests/ -v
```

Tests cover:

- API endpoint behavior
- Input validation
- Error handling
- Tagging functionality
- Storage logic

---

# CI Integration

PromptLab includes a **GitHub Actions CI pipeline** to ensure code quality and reliability.

The CI workflow automatically runs on pushes and pull requests.

The pipeline performs:

- Python environment setup
- Dependency installation
- Static checks (if configured)
- Test execution using pytest

CI configuration is located in:

```
.github/workflows/ci.yml
```

---

# Contribution Guide

Contributions are welcome and encouraged.

## Contribution Workflow

### 1. Fork the Repository

Click **Fork** on GitHub to create your own copy of the repository.

### 2. Clone Your Fork

```shell
git clone https://github.com/<your-username>/PromptLab.git
```

### 3. Create a Feature Branch

```shell
git checkout -b feature/<feature-name>
```

### 4. Implement Your Changes

Follow project coding standards:

- Follow **PEP8**
- Use **type hints**
- Write **Google-style docstrings**
- Keep API routes thin and place business logic in storage/helpers
- Add or update tests for new features
- Update documentation when necessary

### 5. Run Tests Locally

```shell
pytest tests/ -v
```

### 6. Commit Your Changes

Use meaningful commit messages.

Examples:

```
feat: add prompt tagging support
fix: validate collection existence before prompt creation
docs: update README with Docker instructions
```

### 7. Push Your Branch

```shell
git push origin feature/<feature-name>
```

### 8. Open a Pull Request

Submit a Pull Request to the main repository.

Your PR should include:

- Clear description of changes
- Linked issue (if applicable)
- Updated documentation if required
- Tests covering new functionality

PRs will be reviewed for:

- Code quality
- Test coverage
- Documentation completeness
- Architectural consistency

---

# License

This project is licensed under the MIT License.