# Prompt Versions Feature Specification

## Overview and Goals
The Prompt Versions feature enables users to manage different versions of their prompts. This will help track changes and restore prompts to previous states conveniently. 

### Key Goals
- Provide version history for prompts with pagination support.
- Allow viewing specific prompt versions.
- Enable creation of new versions through prompt updates (full or partial changes).
- Support reverting a prompt to a previous version state.
- Optionally enforce limits on the number of versions per prompt (e.g., max_versions) and implement automatic pruning for older versions.

This feature builds on the existing in-memory storage model and Pydantic schemas, maintaining consistency with the architecture of PromptLab.

---

## User Stories & Acceptance Criteria

### 1. Retrieve prompt version history (paginated)
**As a** user  
**I want** to see the version history of a prompt  
**So that** I can understand how it evolved over time  

- **Acceptance criteria**:
    1. A `GET /prompts/{prompt_id}/versions` endpoint delivers a paginated list of versions.
    2. Each version includes an identifier, timestamp, and change details (metadata).
    3. Returns `404` if the prompt does not exist.

---

### 2. View a specific version of a prompt
**As a** user  
**I want** to view specific details of any version  
**So that** I can inspect its content and metadata  

- **Acceptance criteria**:
    1. A `GET /prompts/{prompt_id}/versions/{version_id}` endpoint delivers detailed version data.
    2. Returns `404` if the prompt or version does not exist.

---

### 3. Create a new version by updating a prompt
**As a** user  
**I want** to update the prompt  
**So that** it automatically generates a new version  

- **Acceptance criteria**:
    1. A `PUT /prompts/{prompt_id}` endpoint updates the prompt and creates a version.
    2. Includes metadata about the changes in the version history.
    3. Returns `400` if validation fails.

---

### 4. Revert prompt to a previous version
**As a** user  
**I want** to revert my prompt to a prior version  
**So that** I can roll back changes that are not working  

- **Acceptance criteria**:
    1. A `POST /prompts/{prompt_id}/revert` endpoint reverts the prompt to the specified version.
    2. The current state is saved as a new version before reverting.
    3. Returns `404` if the prompt or version does not exist.

---

### 5. Enforce configurable version limits
**As a** admin  
**I want** to configure a max version limit per prompt  
**So that** older versions are pruned automatically  

- **Acceptance criteria**:
    1. Optional configuration in the storage layer enforces `max_versions_per_prompt`.
    2. Older versions beyond the limit are automatically pruned (based on creation timestamp).

---

## Data Model Changes

### Fields in `PromptVersion` Pydantic Model
Add a new Pydantic model `PromptVersion`:

```python
PromptVersion:
    id: str (unique identifier for the version)
    prompt_id: str (foreign key to the original prompt)
    changed_at: datetime (timestamp of the version creation)
    changes_description: Optional[str] (metadata about the changes; optional)
    content: str (snapshot of the prompt content for this version)
```

### Changes to `Prompt` Pydantic Model
Modify the `Prompt` model:
- Add a `version_count: int` field to track number of versions.
- Add `versions: list[PromptVersion]` for storing associated versions.

---

## API Endpoints

### Endpoint: Retrieve Prompt Version History
- **Path**: `GET /prompts/{prompt_id}/versions`
- **Request Query Params**:
    - `page`: int (default=1)
    - `per_page`: int (default=10)
- **Response**:
    ```json
    {
        "versions": [
            {
                "id": "ver-123",
                "changed_at": "2023-11-01T12:34:56",
                "changes_description": "Updated name and content",
                "content": "New content"
            },
            ...
        ],
        "page": 1,
        "total_pages": 3
    }
    ```
- **Status Codes**:
    - `200` OK
    - `404` Not Found

---

### Endpoint: View Specific Version
- **Path**: `GET /prompts/{prompt_id}/versions/{version_id}`
- **Response**:
    ```json
    {
        "id": "ver-123",
        "changed_at": "2023-11-01T12:34:56",
        "changes_description": "Updated name and content",
        "content": "New content"
    }
    ```
- **Status Codes**:
    - `200` OK
    - `404` Not Found

---

### Endpoint: Update Prompt and Create New Version
- **Path**: `PUT /prompts/{prompt_id}`
- **Request**:
    ```json
    {
        "name": "Updated prompt name",
        "content": "Updated content with details"
    }
    ```
- **Response**:
    ```json
    {
        "id": "ver-123",
        "changed_at": "2023-11-01T12:34:56",
        "changes_description": "Updated name and content",
        "content": "Updated content with details"
    }
    ```
- **Status Codes**:
    - `200` OK
    - `400` Bad Request
    - `404` Not Found

---

### Endpoint: Revert Prompt to Previous Version
- **Path**: `POST /prompts/{prompt_id}/revert`
- **Request**:
    ```json
    {
        "version_id": "ver-123"
    }
    ```
- **Response**:
    ```json
    {
        "id": "ver-456",
        "changed_at": "2023-11-02T10:00:00",
        "content": "Content reverted to version ver-123"
    }
    ```
- **Status Codes**:
    - `200` OK
    - `404` Not Found

---

## Edge Cases
- Requesting versions for non-existent prompts (`404`).
- Requesting non-existent versions (`404`).
- Malformed payload during update or revert (`400`).
- Pruning: What happens when `max_versions_per_prompt` is very low (test behavior).
- Reverting to the currently active version (no-op).

---

## Implementation Steps

### Back-End Architecture:
1. **Data Model**:
    - Add `PromptVersion` model to `models.py`.
    - Modify `Prompt` model to include version tracking.

2. **Storage Layer**:
    - Extend `backend/app/storage.py` to support version tracking:
        - Add function `create_version()` for new versions.
        - Add function `list_versions()` with pagination support.
        - Implement pruning logic for `max_versions_per_prompt`.

3. **API Endpoints**:
    - Create endpoints in `backend/app/api.py`.

4. **Testing**:
    - Write unit tests in `backend/tests/` for:
        - Version creation
        - Pagination logic
        - Revert functionality
        - Edge cases (e.g., pruning)

---

## Additional Notes
- Use in-memory pruning logic for now; integrate with DB when planned.