# PromptLab API Reference

This document provides a comprehensive overview of all the API endpoints available in `backend/app/api.py`, including their usage, parameters, request bodies, responses, and error codes.

---

## Error Codes and Formats

Error codes in the PromptLab API follow standard HTTP status codes.

### Error Response Format
When an error occurs, the API returns JSON responses with the following structure:

```json
{
    "detail": "Error message describing what went wrong"
}
```

### Common Error Codes
- **400**: Bad Request – Malformed payload, invalid input, or business rule violations (e.g., invalid collection references).
- **404**: Not Found – Requested resource not found (e.g., Prompt or Collection not available).
- **422**: Unprocessable Entity – Validation errors (handled automatically by FastAPI and Pydantic).
- **500**: Internal Server Error – Unexpected server-side failure.

---

## Health Check

### GET `/health`
- **Description**: Check the health status and current version of the PromptLab API.
- **Parameters**: None
- **Request Body**: None
- **Response**:
  ```json
  {
    "status": "healthy",
    "version": "1.0.0"
  }
  ```

#### Example Request:
```bash
curl -X GET "http://localhost:8000/health"
```

---

## Prompt Endpoints

### GET `/prompts`
- **Description**: List available prompts with optional filtering by collection, search keywords, or tags.
- **Parameters**:
  - `collection_id` (Optional, query): The ID of the collection to filter prompts by.
  - `search` (Optional, query): A keyword to search within prompt titles and contents.
  - `tags` (Optional, query): Comma-separated list of tags to filter prompts by.
- **Request Body**: None
- **Response**:
  ```json
  {
    "prompts": [
      {
        "id": "prompt-123",
        "title": "Example Title",
        "content": "Example Content",
        "description": "Optional description",
        "collection_id": "col-123",
        "tags": ["tag1", "tag2"],
        "created_at": "2023-11-01T12:00:00Z",
        "updated_at": "2023-11-01T12:00:00Z"
      }
    ],
    "total": 1
  }
  ```

#### Example Requests:
- List all prompts:
  ```bash
  curl -X GET "http://localhost:8000/prompts"
  ```
- Filter prompts by collection:
  ```bash
  curl -X GET "http://localhost:8000/prompts?collection_id=col-123"
  ```
- Search prompts by keyword:
  ```bash
  curl -X GET "http://localhost:8000/prompts?search=hello"
  ```
- Filter prompts by tags:
  ```bash
  curl -X GET "http://localhost:8000/prompts?tags=tag1,tag2"
  ```

---

### GET `/prompts/{prompt_id}`
- **Description**: Retrieve a specific prompt by its ID.
- **Parameters**:
  - `prompt_id` (Required, path): The unique identifier of the prompt to retrieve.
- **Request Body**: None
- **Response**:
  ```json
  {
    "id": "prompt-123",
    "title": "Example Title",
    "content": "Example Content",
    "description": "Optional description",
    "collection_id": "col-123",
    "tags": ["tag1", "tag2"],
    "created_at": "2023-11-01T12:00:00Z",
    "updated_at": "2023-11-01T12:00:00Z"
  }
  ```

#### Example Request:
```bash
curl -X GET "http://localhost:8000/prompts/prompt-123"
```

---

### POST `/prompts`
- **Description**: Create a new prompt in the specified collection.
- **Parameters**: None
- **Request Body**:
  ```json
  {
    "title": "Example Title",
    "content": "Example Content",
    "description": "Optional description",
    "collection_id": "col-123",
    "tags": ["example_tag"]
  }
  ```
- **Response**:
  ```json
  {
    "id": "prompt-123",
    "title": "Example Title",
    "content": "Example Content",
    "description": "Optional description",
    "collection_id": "col-123",
    "tags": ["example_tag"],
    "created_at": "2023-11-01T12:00:00Z",
    "updated_at": "2023-11-01T12:00:00Z"
  }
  ```

#### Example Request:
```bash
curl -X POST "http://localhost:8000/prompts" -H "Content-Type: application/json" \
-d '{"title": "Example Title", "content": "Example Content", "collection_id": "col-123", "tags": ["example_tag"]}'
```

---

### PUT `/prompts/{prompt_id}`
- **Description**: Update all fields of an existing prompt by its ID.
- **Parameters**:
  - `prompt_id` (Required, path): The unique identifier of the prompt to update.
- **Request Body**:
  ```json
  {
    "title": "Updated Title",
    "content": "Updated Content",
    "description": "Updated Description",
    "collection_id": "col-123",
    "tags": ["updated_tag1", "updated_tag2"]
  }
  ```
- **Response**:
  ```json
  {
    "id": "prompt-123",
    "title": "Updated Title",
    "content": "Updated Content",
    "description": "Updated Description",
    "collection_id": "col-123",
    "tags": ["updated_tag1", "updated_tag2"],
    "created_at": "2023-11-01T12:00:00Z",
    "updated_at": "2023-11-01T12:10:00Z"
  }
  ```

#### Example Request:
```bash
curl -X PUT "http://localhost:8000/prompts/prompt-123" -H "Content-Type: application/json" \
-d '{"title": "Updated Title", "content": "Updated Content", "tags": ["updated_tag1"]}'
```

---

### PATCH `/prompts/{prompt_id}`
- **Description**: Partially update specific fields of an existing prompt by ID.
- **Parameters**:
  - `prompt_id` (Required, path): The unique identifier of the prompt to patch.
- **Request Body**:
  ```json
  {
    "content": "Partially Updated Content",
    "tags": ["new_tag"]
  }
  ```
- **Response**:
  ```json
  {
    "id": "prompt-123",
    "title": "Example Title",
    "content": "Partially Updated Content",
    "description": "Optional description",
    "collection_id": "col-123",
    "tags": ["new_tag"],
    "created_at": "2023-11-01T12:00:00Z",
    "updated_at": "2023-11-01T12:10:00Z"
  }
  ```

#### Example Request:
```bash
curl -X PATCH "http://localhost:8000/prompts/prompt-123" -H "Content-Type: application/json" \
-d '{"tags": ["new_tag"]}'
```

---

### DELETE `/prompts/{prompt_id}`
- **Description**: Delete a prompt by its ID.
- **Parameters**:
  - `prompt_id` (Required, path): The unique identifier of the prompt to delete.
- **Request Body**: None
- **Response**: None

#### Example Request:
```bash
curl -X DELETE "http://localhost:8000/prompts/prompt-123"
```

---

## Collection Endpoints

### GET `/collections`
- **Description**: List all collections stored in the system.
- **Parameters**: None
- **Request Body**: None
- **Response**:
  ```json
  {
    "collections": [
      {
        "id": "col-123",
        "name": "Example Collection",
        "description": "Optional description",
        "created_at": "2023-11-01T12:00:00Z",
        "updated_at": "2023-11-01T12:00:00Z"
      }
    ],
    "total": 1
  }
  ```

#### Example Request:
```bash
curl -X GET "http://localhost:8000/collections"
```

---

### GET `/collections/{collection_id}`
- **Description**: Retrieve a specific collection by its ID.
- **Parameters**:
  - `collection_id` (Required, path): The unique identifier of the collection to retrieve.
- **Request Body**: None
- **Response**:
  ```json
  {
    "id": "col-123",
    "name": "Example Collection",
    "description": "Optional description",
    "created_at": "2023-11-01T12:00:00Z",
    "updated_at": "2023-11-01T12:00:00Z"
  }
  ```

#### Example Request:
```bash
curl -X GET "http://localhost:8000/collections/col-123"
```

---

### POST `/collections`
- **Description**: Create a new collection.
- **Parameters**: None
- **Request Body**:
  ```json
  {
    "name": "Example Collection",
    "description": "Optional description"
  }
  ```
- **Response**:
  ```json
  {
    "id": "col-123",
    "name": "Example Collection",
    "description": "Optional description",
    "created_at": "2023-11-01T12:00:00Z",
    "updated_at": "2023-11-01T12:00:00Z"
  }
  ```

#### Example Request:
```bash
curl -X POST "http://localhost:8000/collections" -H "Content-Type: application/json" \
-d '{"name": "Example Collection"}'
```

---

### DELETE `/collections/{collection_id}`
- **Description**: Delete a collection by its ID along with its associated prompts.
- **Parameters**:
  - `collection_id` (Required, path): The unique identifier of the collection to delete.
- **Request Body**: None
- **Response**: None

#### Example Request:
```bash
curl -X DELETE "http://localhost:8000/collections/col-123"