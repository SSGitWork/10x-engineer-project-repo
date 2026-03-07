# Tagging System Specification

## Overview and Goals

The tagging system allows users to label prompts with one or more text-based tags, filter prompts based on tags, and remove tags from prompts. Tags improve organization and searchability of prompts within the application.

Tags are stored directly within the Prompt resource, keeping the system simple and avoiding unnecessary resource fragmentation.

This design integrates tagging with the existing prompt endpoints instead of introducing new dedicated tag endpoints.

### Key Goals
1. Enable users to add one or more tags to prompts.
2. Allow users to filter prompts based on tags.
3. Provide functionality to remove tags.
4. Ensure backward compatibility for prompts without tags.
5. Keep tags simple (text-based, case-insensitive strings, and length-limited).
6. Maintain REST resource consistency by treating tags as a Prompt attribute.

## User Stories with Acceptance Criteria

### User Story 1: Add Tags to a Prompt
**As an AI engineer, I want to label a prompt with one or more tags so that I can categorize it thematically.**

#### Acceptance Criteria:
- Tags can be added when:
   - Creating a prompt
   - Updating a prompt
   - Partially updating a prompt
- Each prompt can have zero or more tags.
- Tags are stored within the prompt resource (tags array).
- Tag strings have validation rules:
   - Case-insensitive.
   - Stored normalized in lowercase.
   - No special symbols (alphanumeric + spaces).
   - Maximum length: 50 characters.
- Duplicate tags are automatically removed.
- Response always returns the updated prompt including tags.

### User Story 2: Filter Prompts by Tags
**As an AI engineer, I want to filter prompts based on one or more tags so that I can find prompts related to specific themes or topics.**

#### Acceptance Criteria:
- Support filtering prompts by one or more tags.
- Return prompts that match any of the provided tags.
- If no matching tags exist, return an empty result set.

### User Story 3: Remove Tags from a Prompt
**As an AI engineer, I want to remove tags from a prompt so that I can declutter its label or update its categorization.**

#### Acceptance Criteria:
- Tags are managed as part of the Prompt resource.
- Removing tags is performed through the existing `PATCH /prompts/{prompt_id}` endpoint.
- The provided `tags` array replaces the current tag set for the prompt.
- Removing a non-existent tag has no side effects (idempotent behavior).
- Response returns the updated prompt including the new tags list.

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

The tagging system extends the existing Prompt resource rather than introducing separate tag endpoints. Tags are treated as a property of the Prompt.

### 1. Create Prompt With Tags

**Method:** `POST`

**URL:** `/prompts`

**Request Body:**
```json
{
  "title": "Example Prompt",
  "content": "This is a test prompt.",
  "collection_id": "collection1",
  "tags": ["example", "ai"]
}
```

**Response (Success, 201):**
```json
{
  "id": "prompt123",
  "title": "Example Prompt",
  "content": "This is a test prompt.",
  "collection_id": "collection1",
  "tags": ["example", "ai"]
}
```

### 2. Update Prompt Tags

**Method:** `PATCH`

**URL:** `/prompts/{prompt_id}`

**Request Body:**
```json
{
  "tags": ["example", "ai"]
}
```

**Response (Success, 200):**

Returns the updated Prompt resource.

### 3. Filter Prompts by Tags

**Method:** `GET`

**URL:** `/prompts`

**Query Parameters:**

```
tags=example,ai
```

**Example Request**

```
GET /prompts?tags=example,ai
```

**Response (Success, 200):**

```
{
  "prompts": [...],
  "total": 2
}
```

Filtering returns prompts that match **ANY** of the provided tags.

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

Implementation follows a **Test Driven Development (TDD)** workflow using the **Red → Green → Refactor** cycle.

### Step 1 — Write Failing Tests (Red)

Create a new test module:

```
backend/tests/test_prompt_tags.py
```

Test scenarios:

- create prompt with tags
- create prompt without tags
- normalize uppercase tags
- remove duplicate tags
- reject tags longer than 50 characters
- update tags via PATCH
- remove tags via PATCH
- filter prompts by single tag
- filter prompts by multiple tags
- filtering when prompts contain no tags

Example test names:

```
test_create_prompt_with_tags_success

test_create_prompt_normalizes_tags

test_patch_prompt_updates_tags

test_patch_prompt_removes_tags

test_filter_prompts_by_single_tag

test_filter_prompts_by_multiple_tags

test_filter_prompts_returns_empty
```

### Step 2 — Update Models (Green)

Modify `PromptBase` in `models.py`:

- add `tags: List[str] = Field(default_factory=list)`
- normalize tags to lowercase
- trim whitespace
- enforce maximum tag length (50)
- remove duplicates

Refactor `PromptUpdate` to support partial updates:

```
class PromptUpdate(BaseModel):
    title: Optional[str]
    content: Optional[str]
    description: Optional[str]
    collection_id: Optional[str]
    tags: Optional[List[str]]
```

### Step 3 — Add Tag Filtering Utility

Add helper in `utils.py`:

```
def filter_prompts_by_tags(prompts: List[Prompt], tags: List[str]) -> List[Prompt]:
    tag_set = set(tags)

    return [
        p for p in prompts
        if p.tags and tag_set.intersection(set(p.tags))
    ]
```

### Step 4 — Update API Layer

Enhance the existing `/prompts` endpoint.

Add query parameter:

```
tags: Optional[str] = None
```

Parse tags:

```
tag_list = [t.strip().lower() for t in tags.split(",")]
```

Call the filtering utility when tags are present.

### Step 5 — Update PATCH Logic

Ensure partial updates preserve existing values:

```
tags = prompt_data.tags if prompt_data.tags is not None else existing.tags
```

### Step 6 — Storage Layer

No storage changes required because tags are stored within the Prompt object.

### Step 7 — Refactor

After tests pass:

- extract reusable tag normalization helpers
- simplify route logic
- ensure consistent validation across models

### Step 8 — Documentation

Add usage examples to API documentation.

Example:

```
curl "http://localhost:8000/prompts?tags=ai,ml"
```

### Step 9 — Backward Compatibility

Existing prompts remain compatible because the field uses:

```
tags: List[str] = Field(default_factory=list)
```

Older prompts will automatically receive an empty tag list.

---