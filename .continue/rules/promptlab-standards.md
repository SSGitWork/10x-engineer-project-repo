---
description: Continue Rules for PromptLab (Python 3.11+, FastAPI, pytest)
---

## 1. Project Context
- Project name: PromptLab
- Purpose: FastAPI-powered backend for managing AI prompts and collections.
- Core modules:
    - backend/app/api.py – FastAPI routes.
    - backend/app/models.py – Pydantic models/schemas.
    - backend/app/storage.py – in-memory storage (future DB placeholder).
    - backend/app/utils.py – shared helpers and utilities.
- Tech stack:
    - Python 3.11+
    - FastAPI
    - Pydantic
    - pytest for testing
    - In-memory persistence (for now)
When generating or modifying code, assume this architecture and keep new code consistent with it.

---

## 2. General Coding Standards
- Follow PEP 8:
    - 4-space indentation
    - Descriptive, meaningful names
    - Aim for line length ≤ 100 characters (wrap earlier where reasonable).
- Use explicit imports (no from x import *).
- Use type hints everywhere:
    - Function arguments and return types must be annotated.
    - Use Optional[...] for nullable values.
    - Keep functions small and focused; prefer extracting logic into helpers in utils.py or suitable modules rather than putting complex logic directly into route handlers.
- Avoid premature optimization; prefer clarity and maintainability.

---

## 3. FastAPI Endpoint Patterns
- Define routes in backend/app/api.py using @app.get, @app.post, @app.put, @app.patch, @app.delete, etc.
- Always specify a response_model on route decorators for deterministic responses.
- FastAPI handlers should be thin:
    - Do validation and orchestration in the route.
    - Delegate business logic to functions in storage.py or utils.py.
- Validate dependencies and referential integrity:
    - Example: ensure referenced collections exist before creating a prompt linked to them.
- Use appropriate status codes:
    - 201 for successful creations.
    - 200 for standard successful reads/updates.
    - 204 for successful deletions with no body.
    - 400 for malformed requests or invalid references.
    - 404 when requested entities do not exist.
    - 500 only for unexpected/unhandled server errors.

**When generating new endpoints:**  
1- Place them in backend/app/api.py.  
2- Add a response_model referencing an appropriate Pydantic model from models.py.  
3- Use Google-style docstrings (see section 5).  
4- Validate input and related entities before calling storage functions.  
5- Raise HTTPException with proper status_code and detail.

---

## 4. Pydantic Model Conventions
- All Pydantic models live in backend/app/models.py.
- Use layered base classes to avoid duplication:
    - Example pattern:
        - PromptBase – shared fields (e.g., name, content, collection_id).
        - PromptCreate(PromptBase) – for create payloads; can enforce required fields.
        - PromptUpdate(PromptBase) – for partial updates (fields often Optional).
        - Prompt(PromptBase) – for responses; includes identifiers and timestamps.
- Use Field(...) for validation constraints:
    - Example: name: str = Field(..., min_length=1, max_length=100)
- Use default factories where appropriate:
    - e.g., id: str = Field(default_factory=generate_id)
    - e.g., created_at: datetime = Field(default_factory=get_current_time)
- Configure response models for ORM compatibility when needed:
    - In Pydantic v1: class Config: orm_mode = True
    - In Pydantic v2: model_config = ConfigDict(from_attributes=True) or equivalent.
- Ensure create/update models don’t expose internal-only fields such as id, created_at, updated_at.

**When adding or modifying models:**
- Follow the *Base, *Create, *Update, and main response model pattern.
- Always add type hints and relevant constraints with Field.
- Keep models cohesive: avoid unrelated fields.

---

## 5. Error Handling Approach
- Use fastapi.HTTPException for API errors; never return bare dicts with error messages.
- Standardize status codes:
    - 404 – entity not found (e.g., missing prompt, missing collection).
    - 400 – invalid payload, invalid reference, or business rule violation.
    - 422 – let FastAPI handle validation errors automatically.
    - 500 – only for unexpected errors and not for expected validation paths.
- Error messages:
    - Use clear and specific detail messages, e.g.:
        - "Prompt not found"
        - "Collection with id 'xyz' does not exist"
- Validate related resources before operations:
    - Do not attempt to create or update entities with invalid or non-existing references.
- Helper functions should:
    - Prefer returning safe defaults (e.g., None) and let the route decide how to convert that into HTTP responses.
    - Avoid raising unexpected exceptions that propagate as 500s without control.

---

## 6. Naming Conventions
- Files & modules: snake_case
    - e.g., storage.py, utils.py, api.py, models.py
- Functions & methods: snake_case verbs and actions
    - e.g., list_prompts, get_collection, create_prompt, update_collection
- Classes: PascalCase
    - e.g., PromptBase, CollectionCreate, Storage
- Pydantic models:
    - <Entity>Base, <Entity>Create, <Entity>Update, <Entity> (response)
- Routes:
    - Plural nouns for resources:
        - /prompts, /collections
    - Identify by path parameter:
        - /prompts/{prompt_id}, /collections/{collection_id}
- Tests:
    - Test modules: test_<feature>.py (e.g., test_api_prompts.py)
    - Test functions: test_<scenario>_<expected>()

Always keep names consistent with existing patterns in the repo. If introducing a new concept, mirror existing naming schemes.

---

## 7. Documentation Requirements (Google-Style Docstrings)
- Every public function, class, and route handler must have a Google-style docstring.
- Docstrings should be concise but explicit about:
    - Purpose/behavior
    - Parameters and types
    - Return type and semantics
    - Possible exceptions (HTTPException, ValueError, etc.)
    - Side effects

- Use this structure:
```python
def create_prompt(prompt_data: PromptCreate) -> Prompt:
    """Create a new prompt in the specified collection.

    Args:
        prompt_data (PromptCreate): Data required to create a new prompt, including
            collection reference and prompt content.

    Returns:
        Prompt: The newly created prompt with generated identifier and timestamps.

    Raises:
        HTTPException: If the referenced collection does not exist or the payload
            fails validation.

    Example:
        >>> payload = PromptCreate(
        ...     name="Greeting",
        ...     content="Hello, world",
        ...     collection_id="col-123"
        ... )
        >>> prompt = create_prompt(prompt_data=payload)
        >>> prompt.name
        'Greeting'
    """
    ...
```

- For route handlers, mention HTTP behavior:
```python
@app.post("/prompts", response_model=Prompt, status_code=status.HTTP_201_CREATED)
async def create_prompt_endpoint(prompt_data: PromptCreate) -> Prompt:
    """Create a new prompt resource.

    This endpoint validates the referenced collection and then creates the prompt in
    the in-memory storage.

    Args:
        prompt_data (PromptCreate): The prompt payload received from the API client.

    Returns:
        Prompt: The created prompt, including its assigned identifier.

    Raises:
        HTTPException: If the collection does not exist or validation fails.
    """
    ...
```

---

## 8. Testing Framework & Requirements (pytest)
- Use pytest for all tests.
- Test files go under a backend/tests/ directory (or existing test structure) using:
    - File naming: test_*.py
    - Function naming: test_<condition>_<expected>()
- Whenever business logic, storage operations, or request/response contracts change:
    - Add or update tests to cover:
        - Success scenarios
        - Error scenarios (e.g., missing collection, invalid payload, not found)
- Use fastapi.testclient.TestClient (or equivalent) to test endpoints:
    - Test both:
        - 2xx cases (happy paths).
        - 4xx / 5xx cases (validation & error paths).
- Keep tests deterministic:
    - Clear or reset in-memory storage between tests.
    - If a global Storage object exists, add fixtures that reset it before each test.
- Aim for tests that:
    - Assert status codes, response bodies, and error messages.
    - Verify validation behavior (e.g., 422 on missing required fields).
    - Verify referential integrity checks (e.g., 400/404 when referencing missing collections).


Example test structure:
```python
from fastapi.testclient import TestClient
from backend.app.api import app

client = TestClient(app)


def test_create_prompt_success():
    # Arrange
    # (create a collection first, or use fixture)
    ...

    # Act
    response = client.post("/prompts", json={
        "name": "Greeting",
        "content": "Hello",
        "collection_id": "col-123"
    })

    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Greeting"
    assert "id" in data
```