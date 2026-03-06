# PromptLab

PromptLab is a tool for storing, organizing, and testing AI prompts in collections.

## Table of Contents
- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation Guide](#installation-guide)
- [API Summary](#api-summary)
- [Usage Examples](#usage-examples)
- [Testing](#testing)
- [Contribution](#contribution)
- [License](#license)

## Project Overview

PromptLab is developed with the aim to streamline the process of managing AI prompts. It supports creating, organizing, and testing prompts, making it easier for AI engineers to collaborate and iterate on prompt designs efficiently.

## Architecture

```
PromptLab/
├── backend/
│   ├── app/
│   │   ├── api.py        # FastAPI routes
│   │   ├── models.py     # Pydantic models/schemas
│   │   ├── storage.py    # In-memory storage (future DB placeholder)
│   │   ├── utils.py      # Shared helpers and utilities
└── tests/
    ├── test_api_prompts.py  # Tests for prompt API operations
```

## Prerequisites

- Python 3.11+
- pip (Python package installer)
- Git 2.40+

## Installation Guide

1. **Clone the repository:**
   ```shell
   git clone <repository-url>
   ```

2. **Navigate to the project directory:**
   ```shell
   cd PromptLab
   ```

3. **Create a virtual environment:**
   ```shell
   python -m venv venv
   ```

4. **Activate the virtual environment:**
   - On Windows:
     ```shell
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```shell
     source venv/bin/activate
     ```

5. **Install the dependencies:**
   ```shell
   pip install -r requirements.txt
   ```

## API Summary

PromptLab features a RESTful API, powered by FastAPI, offering the following endpoints:

- **Prompts:**
  - `GET /prompts`: List all prompts
  - `POST /prompts`: Create a new prompt
  - `GET /prompts/{prompt_id}`: Retrieve a specific prompt
  - `PUT /prompts/{prompt_id}`: Update a specific prompt
  - `DELETE /prompts/{prompt_id}`: Delete a specific prompt

- **Collections:**
  - `GET /collections`: List all collections
  - `POST /collections`: Create a new collection
  - `GET /collections/{collection_id}`: Retrieve a specific collection
  - `PUT /collections/{collection_id}`: Update a specific collection
  - `DELETE /collections/{collection_id}`: Delete a specific collection

## Usage Examples

### Starting the Application

To start the FastAPI application, run the following command:

```shell
uvicorn backend.app.api:app --reload
```

The application will be available at `http://127.0.0.1:8000`.

### Sample Request

To create a new prompt:

```json
POST /prompts
{
  "name": "SamplePrompt",
  "content": "This is a sample prompt with variable {{input}}",
  "collection_id": "col-123"
}
```

### Testing

Run the test suite with pytest:

```shell
pytest
```

## Contribution

If you're interested in contributing to PromptLab, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
