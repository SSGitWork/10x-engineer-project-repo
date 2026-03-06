# Tagging System Specification

## Overview and Goals

The tagging system allows users to label prompts with one or more text-based tags, filter prompts based on tags, and remove tags from prompts. Tags improve organization and searchability of prompts within the application. Tags are stored as part of the prompt data, enabling simple backward compatibility for existing prompts that do not support tags.

### Key Goals
1. Enable users to add one or more tags to prompts.
2. Allow users to filter prompts by tags.
3. Provide functionality to remove tags.
4. Ensure backward compatibility for prompts without tags.
5. Keep tags simple (text-based, case-insensitive strings, and length-limited).

## User Stories with Acceptance Criteria

### User Story 1: Add Tags to a Prompt
**As an AI engineer, I want to label a prompt with one or more tags so that I can categorize it thematically.**

#### Acceptance Criteria:
- Tags can be added to new and existing prompts.
- Each prompt can have zero or more tags.
- Tags are stored within the prompt resource (`tags` array).
- Tag strings have simple validation:
  - Case-insensitive (e.g., "AI" and "ai" are treated the same).
  - No special symbols, but spaces are allowed.
  - Maximum tag length: 50 characters.
- Response includes the updated prompt object with tag information.

### User Story 2: Filter Prompts by Tags
**As an AI engineer, I want to filter prompts based on one or more tags so that I can find prompts related to specific themes or topics.**

#### Acceptance Criteria:
- Support filtering prompts by one or more tags.
- Return prompts that match any of the provided tags.
- If no matching tags exist, return an empty result set.

### User Story 3: Remove Tags from a Prompt
**As an AI engineer, I want to remove tags from a prompt so that I can declutter its label or update its categorization.**

#### Acceptance Criteria:
- Users can remove one or more tags from an existing prompt.
- Removing a non-existent tag has no effect on the prompt’s tags (idempotent operation).
- Response includes the updated prompt object with tag information.

### User Story 4: Backward Compatibility
**As an AI engineer, I want to ensure that existing prompts without tags remain functional so that the system works seamlessly without errors.**

#### Acceptance Criteria:
- Prompts without tags can still be fetched, updated, and deleted.
- Filtering prompts by tags gracefully returns an empty result set for prompts lacking tags.

---

## Data Model Changes

### Existing Prompt Model:
```python
class PromptBase(BaseModel):
    id: str
    name: str
    content: str
    collection_id: str
    # Additional fields like created_at
```

### Updated Prompt Model:
```python
class PromptBase(BaseModel):
    id: str
    name: str
    content: str
    collection_id: str
    tags: Optional[List[str]] = Field(default_factory=list)
    # Additional fields like created_at

    @validator("tags", each_item=True)
    def validate_tag(cls, tag: str) -> str:
        if len(tag) > 50:
            raise ValueError("Tag length exceeds 50 characters")
        return tag.lower()  # Normalize tags to lowercase
```

- **Field Additions:**
  - `tags`: A list of case-insensitive strings representing labels associated with the prompt.
  - Validation ensures case normalization and enforces length limits.

---

## API Endpoints

### 1. Add Tags to Prompt
**Method:** `PATCH`  
**URL:** `/prompts/{prompt_id}/tags`  
**Request Body:**  
```json
{
    "tags": ["example", "ai"]
}
```
**Response (Success, 200):**  
```json
{
    "id": "prompt123",
    "name": "Example Prompt",
    "content": "This is a test prompt.",
    "collection_id": "collection1",
    "tags": ["example", "ai"]
}
```

### 2. Remove Tags from Prompt
**Method:** `PATCH`  
**URL:** `/prompts/{prompt_id}/tags/remove`  
**Request Body:**  
```json
{
    "tags": ["example"]
}
```
**Response (Success, 200):**  
```json
{
    "id": "prompt123",
    "name": "Example Prompt",
    "content": "This is a test prompt.",
    "collection_id": "collection1",
    "tags": ["ai"]
}
```

### 3. Filter Prompts by Tags
**Method:** `GET`  
**URL:** `/prompts/filter`  
**Query Parameters:** `tags=example,ai`  
**Response (Success, 200):**  
```json
[
    {
        "id": "prompt123",
        "name": "Example Prompt",
        "content": "This is a test prompt.",
        "collection_id": "collection1",
        "tags": ["example", "ai"]
    },
    {
        "id": "prompt124",
        "name": "Another Prompt",
        "content": "Another test prompt.",
        "collection_id": "collection2",
        "tags": ["ai"]
    }
]
```

---

## Edge Cases Considered
1. **Empty Tags Field:**
   - Prompts without tags are fully operational.
   - API gracefully handles missing or empty `tags` in filter operations.

2. **Case Sensitivity:**
   - Tags are normalized to lowercase.

3. **Invalid Tags:**
   - Tags exceeding 50 characters are rejected with validation errors (`422 Unprocessable Entity`).

4. **Duplicate Tags:**
   - Duplicate tags in the same prompt are eliminated automatically (`["ai", "ai"]` -> `["ai"]`).

5. **Non-Existent Tags During Removal:**
   - Removal silently does nothing if a tag doesn't exist on the prompt.

6. **Filtering Validation:**
   - Filtering works correctly for compound tag searches or prompts without tags.

---

## Implementation Steps

1. **Update Models:**
   - Add `tags` field to `PromptBase` with validation for length and normalization.

2. **Storage Updates:**
   - Extend storage to handle tag updates within the prompt object.
   - Implement tag filtering logic for retrieving matching prompts.

3. **API Enhancements:**
   - Add endpoints for tag addition, removal, and filtering.

4. **Testing:**
   - Write tests to cover all user stories and edge cases:
     - Add/remove tags.
     - Filter by tags.
     - Backward compatibility.

5. **Documentation Updates:**
   - Update API docs to include the endpoints for tagging functionalities.

6. **Validate Backward Compatibility:**
   - Ensure existing prompts without tags load correctly.

---