"""FastAPI routes for PromptLab"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from app.models import (
    Prompt, PromptCreate, PromptUpdate,
    Collection, CollectionCreate,
    PromptList, CollectionList, HealthResponse,
    get_current_time
)
from app.storage import storage
from app.utils import (
    query_prompts,
    parse_tags_query
)
from app import __version__


app = FastAPI(
    title="PromptLab API",
    description="AI Prompt Engineering Platform",
    version=__version__
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============== Health Check ==============

@app.get("/health", response_model=HealthResponse)
def health_check():
    """Return the health status of the PromptLab API.

    This endpoint provides a lightweight check to confirm that the API service
    is running and responsive. It also returns the currently deployed API
    version so clients can verify compatibility.

    Args:
        None: This endpoint does not accept any parameters.
    Returns:
        HealthResponse: An object containing the service health status and the
        current API version.

    Example:
        Request:
            curl -X GET "http://localhost:8000/health"

        Response:
            {
                "status": "healthy",
                "version": "1.0.0"
            }
    """
    return HealthResponse(status="healthy", version=__version__)


# ============== Prompt Endpoints ==============

@app.get("/prompts", response_model=PromptList)
def list_prompts(
    collection_id: Optional[str] = None,
    search: Optional[str] = None,
    tags: Optional[str] = None
):
    """List prompts with optional filtering by collection, search term, and tags.

    This endpoint retrieves all prompts from storage and applies optional
    filtering logic. Clients may filter prompts by collection ID, search
    for keywords within prompt titles and contents, and filter by tags
    provided as a comma-separated query string.

    Args:
        collection_id (Optional[str]): The unique identifier of a collection.
            When provided, only prompts belonging to this collection are returned.
        search (Optional[str]): A keyword used to search within prompt titles
            and contents. Matching prompts containing the keyword are returned.
        tags (Optional[str]): A comma-separated list of tags used to filter
            prompts. Only prompts containing one or more of these tags will
            be included in the results.

    Returns:
        PromptList: An object containing the filtered list of prompts and the
        total number of results returned.
    Example:
        List all prompts:
        curl -X GET "http://localhost:8000/prompts"

        Filter prompts by collection:
        curl -X GET "http://localhost:8000/prompts?collection_id=col-123"

        Search prompts by keyword:
            curl -X GET "http://localhost:8000/prompts?search=assistant"

        Filter prompts by tags:
            curl -X GET "http://localhost:8000/prompts?tags=python,ai"
    """
    prompts = storage.get_all_prompts()

    tag_list = parse_tags_query(tags) if tags else None

    prompts = query_prompts(
        prompts=prompts,
        collection_id=collection_id,
        search=search,
        tags=tag_list
    )

    return PromptList(prompts=prompts, total=len(prompts))

@app.get("/prompts/{prompt_id}", response_model=Prompt)
def get_prompt(prompt_id: str) -> Prompt:
    """Retrieve a specific prompt by its ID.

    This endpoint looks up a prompt in the in-memory storage using the provided
    prompt identifier and returns it if found.

    Args:
        prompt_id (str): The unique identifier of the prompt to retrieve.

    Returns:
        Prompt: The prompt associated with the provided identifier.

    Example:
        Request:
        curl -X GET "http://localhost:8000/prompts/prompt-123"

        Response:
            {
                "id": "prompt-123",
                "title": "Greeting",
                "content": "Hello, world",
                "description": "Simple greeting prompt",
                "collection_id": "col-123",
                "tags": ["example"],
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            }
    """
    prompt = storage.get_prompt(prompt_id)    
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt

@app.post("/prompts", response_model=Prompt, status_code=status.HTTP_201_CREATED)
def create_prompt(prompt_data: PromptCreate) -> Prompt:
    """Create a new prompt resource.

    This endpoint validates that the referenced collection exists (if a
    collection_id is provided) and then creates the prompt in the in-memory
    storage. The created prompt will include a generated identifier and
    timestamps.
    Args:
        prompt_data (PromptCreate): Payload containing the data required to
            create a prompt, including title, content, optional description,
            optional collection_id, and optional tags.
    Returns:
        Prompt: The newly created prompt including its generated id,
        created_at timestamp, and updated_at timestamp.

    Raises:
        HTTPException: If the referenced collection_id is provided but does
        not correspond to an existing collection.

    Example:
        Request:
            curl -X POST "http://localhost:8000/prompts" \
            -H "Content-Type: application/json" \
            -d '{
                "title": "Greeting",
                "content": "Hello, world",
                "description": "Simple greeting prompt",
                "collection_id": "col-123",
                "tags": ["example", "intro"]
            }'

        Response:
            {
                "id": "prompt-abc123",
                "title": "Greeting",
                "content": "Hello, world",
                "description": "Simple greeting prompt",
                "collection_id": "col-123",
                "tags": ["example", "intro"],
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            }
    """
    # Validate collection exists if provided
    if prompt_data.collection_id and not storage.collection_exists(prompt_data.collection_id):
        raise HTTPException(status_code=404, detail="Collection not found")
    
    prompt = Prompt(**prompt_data.model_dump())
    return storage.create_prompt(prompt)

@app.put("/prompts/{prompt_id}", response_model=Prompt)
def update_prompt(prompt_id: str, prompt_data: PromptUpdate) -> Prompt:
    """Fully update an existing prompt.

    This endpoint replaces the fields of an existing prompt with the values
    provided in the request payload. The prompt must already exist in storage.
    If a collection_id is supplied, the endpoint validates that the referenced
    collection exists before applying the update. The original prompt ID and
    created_at timestamp are preserved, while updated_at is refreshed.
    Args:
        prompt_id (str): The unique identifier of the prompt to update.
        prompt_data (PromptUpdate): The new prompt data containing fields such
            as title, content, optional description, optional collection_id,
            and optional tags.

    Returns:
        Prompt: The fully updated prompt object including its identifier and
        updated timestamps.

    Raises:
        HTTPException: If the prompt does not exist.
        HTTPException: If a provided collection_id does not correspond to an
            existing collection.

    Example:
        Update a prompt with ID "prompt-123":
            curl -X PUT "http://localhost:8000/prompts/prompt-123" \
            -H "Content-Type: application/json" \
            -d '{
                "title": "Updated Title",
                "content": "New content",
                "description": "Updated description",
                "collection_id": "col-456",
                "tags": ["ai", "assistant"]
            }'
    """
    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    # Validate collection if provided
    if prompt_data.collection_id and not storage.collection_exists(prompt_data.collection_id):
        raise HTTPException(status_code=404, detail="Collection not found")
    
    updated_prompt = Prompt(
        id=existing.id,
        title=prompt_data.title,
        content=prompt_data.content,
        description=prompt_data.description,
        collection_id=prompt_data.collection_id,
        tags=prompt_data.tags or [],
        created_at=existing.created_at,
        updated_at=get_current_time()
    )
    
    return storage.update_prompt(prompt_id, updated_prompt)

@app.patch("/prompts/{prompt_id}", response_model=Prompt)
def patch_prompt(prompt_id: str, prompt_data: PromptUpdate) -> Prompt:
    """Partially update an existing prompt.

    This endpoint updates only the fields provided in the request payload.
    The prompt must already exist in storage. If a new ``collection_id`` is
    provided, the endpoint validates that the referenced collection exists
    before applying the update. The original prompt ID and ``created_at``
    timestamp are preserved, while ``updated_at`` is refreshed.
    Args:
        prompt_id (str): The unique identifier of the prompt to update.
        prompt_data (PromptUpdate): A partial prompt payload containing only
            the fields that should be updated. Fields not included in the
            payload remain unchanged.

    Returns:
        Prompt: The updated prompt object after applying the partial changes.
    Example:
        Partially update a prompt's content and description:
        curl -X PATCH "http://localhost:8000/prompts/prompt-123" \
        -H "Content-Type: application/json" \
        -d '{
            "content": "Updated Content",
            "description": "New description"
        }'
    """
    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    # Validate collection if collection_id is being updated
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")

    update_data = prompt_data.model_dump(exclude_unset=True)

    updated_prompt = existing.model_copy(update=update_data)
    updated_prompt.updated_at = get_current_time()

    return storage.update_prompt(prompt_id, updated_prompt)


@app.delete("/prompts/{prompt_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_prompt(prompt_id: str) -> None:
    """Delete an existing prompt resource by its identifier.
    This endpoint removes a prompt from the in-memory storage. If the specified
    prompt does not exist, the request will return a 404 error. A successful
    deletion returns no response body.
    Args:
        prompt_id (str): The unique identifier of the prompt that should be
            deleted from storage.

    Returns:
        None: No content is returned when the deletion succeeds.
    Example:
        Delete a prompt with ID "prompt-123":

        curl -X DELETE "http://localhost:8000/prompts/prompt-123"
    """
    if not storage.delete_prompt(prompt_id):
        raise HTTPException(status_code=404, detail="Prompt not found")
    return None


# ============== Collection Endpoints ==============

@app.get("/collections", response_model=CollectionList)
def list_collections() -> CollectionList:
    """Retrieve all collections stored in the system.

    This endpoint returns every collection currently available in the
    in-memory storage along with a count of the total number of collections.
    It provides a simple way for clients to enumerate existing collections
    before performing operations such as creating prompts within them.
    Args:
        None: This endpoint does not accept any parameters.

    Returns:
        CollectionList: An object containing the list of all collections and
        the total number of collections stored.
    Example:
        Request:
        curl -X GET "http://localhost:8000/collections"

        Response:
            {
                "collections": [
                    {
                        "id": "col-123",
                        "name": "Examples",
                        "description": "Example prompts",
                        "created_at": "2024-01-01T00:00:00Z"
                    }
                ],
                "total": 1
            }
    """
    collections = storage.get_all_collections()
    return CollectionList(collections=collections, total=len(collections))


@app.get("/collections/{collection_id}", response_model=Collection)
def get_collection(collection_id: str) -> Collection:
    """Retrieve a single collection by its identifier.

    This endpoint looks up a collection in the in-memory storage using the
    provided collection ID and returns it if found. If the collection does
    not exist, a 404 error is returned.
    Args:
        collection_id (str): The unique identifier of the collection that
            should be retrieved from storage.

    Returns:
        Collection: The collection associated with the provided identifier.

    Raises:
        HTTPException: If no collection exists with the given ID.

    Example:
        Request:
        curl -X GET "http://localhost:8000/collections/col-123"

        Response:
            {
                "id": "col-123",
                "name": "Example Collection",
                "description": "Example prompts",
                "created_at": "2024-01-01T00:00:00Z"
            }
    """
    collection = storage.get_collection(collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection


@app.post("/collections", response_model=Collection, status_code=status.HTTP_201_CREATED)
def create_collection(collection_data: CollectionCreate) -> Collection:
    """Create a new collection resource.

    This endpoint creates a new collection in the in-memory storage using the
    provided payload. A unique identifier and creation timestamp are generated
    automatically before the collection is persisted.
    Args:
        collection_data (CollectionCreate): The payload containing the data
            required to create a collection, including the collection name
            and an optional description.

    Returns:
        Collection: The newly created collection including its generated
        identifier and creation timestamp.

    Example:
        Create a new collection using curl:
            curl -X POST "http://localhost:8000/collections" \
            -H "Content-Type: application/json" \
            -d '{
                "name": "New Collection",
                "description": "Collection Description"
            }'
    """
    collection = Collection(**collection_data.model_dump())
    return storage.create_collection(collection)


@app.delete("/collections/{collection_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_collection(collection_id: str) -> None:
    """Delete an existing collection and all prompts associated with it.

    This endpoint removes a collection from the in-memory storage and ensures
    that any prompts linked to the collection are also deleted. If the
    specified collection does not exist, the request returns a 404 error.
    Args:
        collection_id (str): The unique identifier of the collection that
            should be deleted along with its associated prompts.

    Returns:
        None: No response body is returned when the deletion succeeds.
    Example:
        Delete a collection with ID "col-123":
        curl -X DELETE "http://localhost:8000/collections/col-123"
    """
    if not storage.delete_collection_with_prompts(collection_id):
        raise HTTPException(status_code=404, detail="Collection not found")

    return None
