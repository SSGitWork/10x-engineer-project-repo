"""FastAPI routes for PromptLab"""

from fastapi import FastAPI, HTTPException
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
    sort_prompts_by_date,
    filter_prompts_by_collection,
    search_prompts,
    filter_prompts_by_tags,
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
    """Check the health status of the PromptLab API.

    This route provides quick insight into the service status and current version.

    Returns:
        HealthResponse: The health status and version of the API.
    """
    return HealthResponse(status="healthy", version=__version__)


# ============== Prompt Endpoints ==============

@app.get("/prompts", response_model=PromptList)
def list_prompts(
    collection_id: Optional[str] = None,
    search: Optional[str] = None,
    tags: Optional[str] = None
):
    """List available prompts with optional filtering and searching.

    Args:
        collection_id (Optional[str]): The ID of the collection to filter prompts by.
        search (Optional[str]): A keyword to search for within prompt titles and contents.

    Returns:
        PromptList: A list of prompts after filtering and/or searching.

    Example:
        To list all prompts:
        curl -X GET "http://localhost:8000/prompts"

        To list prompts in a specific collection:
        curl -X GET "http://localhost:8000/prompts?collection_id=col-123"

        To search prompts by keyword:
        curl -X GET "http://localhost:8000/prompts?search=Hello"
    """
    prompts = storage.get_all_prompts()
    
    # Filter by collection if specified
    if collection_id:
        prompts = filter_prompts_by_collection(prompts, collection_id)
    
        # Search if query provided
    if search:
        prompts = search_prompts(prompts, search)

    # Filter by tags
    if tags:
        tag_list = parse_tags_query(tags)
        prompts = filter_prompts_by_tags(prompts, tag_list)

    # Sort by date (newest first)
    prompts = sort_prompts_by_date(prompts, descending=True)
    
    return PromptList(prompts=prompts, total=len(prompts))


@app.get("/prompts/{prompt_id}", response_model=Prompt)
def get_prompt(prompt_id: str):
    """Retrieve a specific prompt by its ID.

    This endpoint fetches a prompt from storage using the provided prompt ID.

    Args:
        prompt_id (str): The unique identifier of the prompt to retrieve.

    Returns:
        Prompt: The prompt with the specified ID, if found.

    Raises:
        HTTPException: If the prompt with the given ID does not exist.

    Example:
        To get a prompt with ID "prompt-123":
        curl -X GET "http://localhost:8000/prompts/prompt-123"
    """
    prompt = storage.get_prompt(prompt_id)    
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt


@app.post("/prompts", response_model=Prompt, status_code=201)
def create_prompt(prompt_data: PromptCreate):
    """Create a new prompt in the specified collection.

    This endpoint validates the referenced collection and creates the prompt in
    in-memory storage.

    Args:
        prompt_data (PromptCreate): Data required to create a new prompt, including
            collection reference and prompt content.

    Returns:
        Prompt: The newly created prompt with generated identifier and timestamps.

    Raises:
        HTTPException: If the referenced collection does not exist or the payload fails validation.

    Example:
        To create a new prompt with collection ID "col-123":
        curl -X POST "http://localhost:8000/prompts" -H "Content-Type: application/json" \
        -d '{"title": "Greeting", "content": "Hello, world", "collection_id": "col-123"}'
    """
    # Validate collection exists if provided
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")
    
    prompt = Prompt(**prompt_data.model_dump())
    return storage.create_prompt(prompt)


@app.put("/prompts/{prompt_id}", response_model=Prompt)
def update_prompt(prompt_id: str, prompt_data: PromptUpdate):
    """Update a prompt with all fields.

    This endpoint replaces the entire prompt with new data if valid.
    It ensures the prompt exists and optionally validates the collection reference.

    Args:
        prompt_id (str): The unique identifier of the prompt to update.
        prompt_data (PromptUpdate): The new data for the prompt, replacing existing fields.

    Returns:
        Prompt: The updated prompt including its identifier and timestamps.

    Raises:
        HTTPException: If the prompt or the referenced collection does not exist.

    Example:
        To update a prompt with ID "prompt-123":
        curl -X PUT "http://localhost:8000/prompts/prompt-123" -H "Content-Type: application/json" \
        -d '{"title": "Updated Title", "content": "New content", "collection_id": "col-456"}'
    """
    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    # Validate collection if provided
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")
    
    updated_prompt = Prompt(
        id=existing.id,
        title=prompt_data.title,
        content=prompt_data.content,
        description=prompt_data.description,
        collection_id=prompt_data.collection_id,
        created_at=existing.created_at,
        updated_at=get_current_time()
    )
    
    return storage.update_prompt(prompt_id, updated_prompt)

@app.patch("/prompts/{prompt_id}", response_model=Prompt)
def patch_prompt(prompt_id: str, prompt_data: PromptUpdate):
    """Partially update fields of an existing prompt.

    This endpoint allows updating specific fields of a prompt.
    It checks if the prompt exists and validates the collection reference if provided.

    Args:
        prompt_id (str): The unique identifier of the prompt to patch.
        prompt_data (PromptUpdate): The fields to update for the prompt if present.

    Returns:
        Prompt: The partially updated prompt with its identifier and timestamps.

    Raises:
        HTTPException: If the prompt or the referenced collection does not exist.

    Example:
        To partially update a prompt with ID "prompt-123":
        curl -X PATCH "http://localhost:8000/prompts/prompt-123" -H "Content-Type: application/json" \
        -d '{"content": "Updated Content", "description": "New description"}'
    """
    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    # Validate collection if collection_id is being updated
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")

    # Partially update fields if provided
    updated_prompt = Prompt(
        id=existing.id,
        title=prompt_data.title if prompt_data.title is not None else existing.title,
        content=prompt_data.content if prompt_data.content is not None else existing.content,
        description=prompt_data.description if prompt_data.description is not None else existing.description,
        collection_id=prompt_data.collection_id if prompt_data.collection_id is not None else existing.collection_id,
        tags=prompt_data.tags if prompt_data.tags is not None else existing.tags,
        created_at=existing.created_at,
        updated_at=get_current_time()
    )

    return storage.update_prompt(prompt_id, updated_prompt)


@app.delete("/prompts/{prompt_id}", status_code=204)
def delete_prompt(prompt_id: str):
    """Delete a prompt by its ID.

    This endpoint removes a prompt from the in-memory storage if it exists.
    It will return a 404 error if the prompt is not found.

    Args:
        prompt_id (str): The unique identifier of the prompt to delete.

    Returns:
        None: This endpoint returns no content in case of a successful deletion.

    Raises:
        HTTPException: If the prompt with the given ID does not exist.

    Example:
        To delete a prompt with ID "prompt-123":
        curl -X DELETE "http://localhost:8000/prompts/prompt-123"
    """
    if not storage.delete_prompt(prompt_id):
        raise HTTPException(status_code=404, detail="Prompt not found")
    return None


# ============== Collection Endpoints ==============

@app.get("/collections", response_model=CollectionList)
def list_collections():
    """List all available collections.

    This endpoint retrieves all collections stored in the system.

    Returns:
        CollectionList: A list of collections including a count of total records.

    Example:
        To list all collections:
        curl -X GET "http://localhost:8000/collections"
    """
    collections = storage.get_all_collections()
    return CollectionList(collections=collections, total=len(collections))


@app.get("/collections/{collection_id}", response_model=Collection)
def get_collection(collection_id: str):
    """Retrieve a specific collection by its ID.

    This endpoint fetches a collection from storage using the provided collection ID.

    Args:
        collection_id (str): The unique identifier of the collection to retrieve.

    Returns:
        Collection: The collection with the specified ID, if found.

    Raises:
        HTTPException: If the collection with the given ID does not exist.

    Example:
        To get a collection with ID "col-123":
        curl -X GET "http://localhost:8000/collections/col-123"
    """
    collection = storage.get_collection(collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection


@app.post("/collections", response_model=Collection, status_code=201)
def create_collection(collection_data: CollectionCreate):
    """Create a new collection.

    This endpoint adds a new collection to the in-memory storage using the provided
    data.

    Args:
        collection_data (CollectionCreate): The data required to create a new collection.

    Returns:
        Collection: The newly created collection with generated identifier.

    Example:
        To create a new collection:
        curl -X POST "http://localhost:8000/collections" -H "Content-Type: application/json" \
        -d '{"name": "New Collection", "description": "Collection Description"}'
    """
    collection = Collection(**collection_data.model_dump())
    return storage.create_collection(collection)


@app.delete("/collections/{collection_id}", status_code=204)
def delete_collection(collection_id: str):
    """Delete a collection and its associated prompts by collection ID.

    This endpoint deletes a specified collection and ensures that all prompts
    associated with the collection are also deleted from storage.

    Args:
        collection_id (str): The unique identifier of the collection to delete.

    Returns:
        None: This endpoint does not return a content response for successful deletions.

    Raises:
        HTTPException: If the collection with the given ID does not exist.

    Example:
        To delete a collection with ID "col-123":
        curl -X DELETE "http://localhost:8000/collections/col-123"
    """
    # First, fetch the collection to check its existence and get associated prompts
    collection = storage.get_collection(collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    
    # Retrieve all prompts with the collection_id to handle them
    prompts = storage.get_prompts_by_collection(collection_id)

    # Delete or handle the associated prompts as needed
    for prompt in prompts:
        storage.delete_prompt(prompt.id)

    # Now, delete the collection itself
    storage.delete_collection(collection_id)
    return None
