"""Pydantic models for PromptLab"""

from datetime import datetime, UTC
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator, ConfigDict
from uuid import uuid4
from app.utils import normalize_tags

def generate_id() -> str:
    """Generate a unique identifier for a resource.

    This function creates a new UUID4-based identifier and returns it as a
    string. It is typically used as the default factory for model `id`
    fields in Prompt and Collection entities.
    Args:
        None
    Returns:
        str: A randomly generated UUID4 string representing a unique identifier.
    Example:
        >>> new_id = generate_id()
        >>> isinstance(new_id, str)
        True
    """
    return str(uuid4())


def get_current_time() -> datetime:
    """Return the current UTC timestamp.

    This helper function retrieves the current datetime in UTC and is commonly
    used as the default factory for `created_at` and `updated_at` fields in
    application models.

    Args:
        None

    Returns:
        datetime: The current timezone-aware datetime in UTC.

    Example:
        >>> now = get_current_time()
        >>> now.tzinfo is not None
        True
    """
    return datetime.now(UTC)

# ============== Prompt Models ==============

class PromptBase(BaseModel):
    """Base model for defining shared prompt attributes.

    This model contains the core fields that describe a prompt. It is used as the
    foundation for prompt-related schemas such as creation, update, and response
    models. Validation rules ensure that prompt titles and content meet minimum
    length requirements and that tags are normalized before storage.

    Attributes:
        title (str): Human-readable title of the prompt. Must be between
            1 and 200 characters.
        content (str): Main textual content of the prompt. Must contain
            at least one character.
        description (Optional[str]): Optional description providing
            additional context about the prompt. Maximum length is
            500 characters.
        collection_id (Optional[str]): Identifier of the collection this
            prompt belongs to. May be None if the prompt is not associated
            with a collection.
        tags (List[str]): List of tags used for categorizing or searching
            prompts. Tags are normalized using the shared `normalize_tags`
            utility before validation.

    Example:
        >>> prompt = PromptBase(
        ...     title="Example Prompt",
        ...     content="Write a short poem about the ocean.",
        ...     description="Creative writing prompt",
        ...     collection_id="col-123",
        ...     tags=["Poetry", " Writing ", "Ocean"]
        ... )
        >>> prompt.tags
        ['poetry', 'writing', 'ocean']
    """
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    description: Optional[str] = Field(None, max_length=500)
    collection_id: Optional[str] = None
    tags: List[str] = Field(default_factory=list)

    @field_validator("tags", mode="before")
    @classmethod
    def normalize_tags_validator(cls, tags):
        return normalize_tags(tags)


class PromptCreate(PromptBase):
    """Model used when creating a new prompt.

    This schema is typically used as the request body for API endpoints that
    create prompt resources. It inherits all validation and fields from
    PromptBase while excluding system-managed fields such as identifiers
    and timestamps.

    Attributes:
        title (str): Title of the prompt.
        content (str): Main textual prompt content.
        description (Optional[str]): Optional descriptive text about the prompt.
        collection_id (Optional[str]): Identifier of the collection the prompt
            should belong to.
        tags (List[str]): Optional list of tags used to categorize the prompt.
    Example:
        >>> payload = PromptCreate(
        ...     title="Greeting Generator",
        ...     content="Generate a friendly greeting message.",
        ...     tags=["greeting", "assistant"]
        ... )
        >>> payload.title
        'Greeting Generator'
    """
    pass


class PromptUpdate(BaseModel):
    """Model for partially updating an existing prompt.

    All fields are optional. Only fields provided in the request payload
    should be updated. Fields that are omitted will retain their existing
    values in storage. Tag values are normalized before validation if they
    are provided.

    Attributes:
        title (Optional[str]): Updated title for the prompt. Must be between
            1 and 200 characters if provided.
        content (Optional[str]): Updated prompt content.
        description (Optional[str]): Updated description text with a maximum
            length of 500 characters.
        collection_id (Optional[str]): Updated collection identifier for
            the prompt.
        tags (Optional[List[str]]): Updated list of tags. Tags are normalized
            using the shared `normalize_tags` utility.

    Example:
        >>> update_data = PromptUpdate(
        ...     title="Updated Prompt Title",
        ...     tags=["updated", "example"]
        ... )
        >>> update_data.title
        'Updated Prompt Title'
    """

    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = Field(None, max_length=500)
    collection_id: Optional[str] = None
    tags: Optional[List[str]] = None

    @field_validator("tags", mode="before")
    @classmethod
    def normalize_tags_validator(cls, tags):
        if tags is None:
            return tags
        return normalize_tags(tags)

class Prompt(PromptBase):
    """Represents a complete prompt resource including system metadata.

    This model extends PromptBase by adding system-managed fields such as
    a unique identifier and timestamps. It is typically returned by API
    endpoints and represents the stored form of a prompt in the application.
    Attributes:
        id (str): Unique identifier for the prompt. Automatically generated
            using a UUID4 string when a new prompt is created.
        created_at (datetime): UTC timestamp indicating when the prompt
            was initially created.
        updated_at (datetime): UTC timestamp indicating the most recent
            update made to the prompt.

    Example:
        >>> prompt = Prompt(
        ...     title="Final Prompt",
        ...     content="Complete prompt content.",
        ...     description="Example prompt",
        ...     tags=["example", "demo"]
        ... )
        >>> prompt.id
        'generated-uuid'
        >>> isinstance(prompt.created_at, datetime)
        True
    """
    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)
    updated_at: datetime = Field(default_factory=get_current_time)

    model_config = ConfigDict(from_attributes=True)


# ============== Collection Models ==============

class CollectionBase(BaseModel):
    """Base schema containing shared collection attributes.

    This model defines the core fields used to describe a collection.
    It serves as the foundation for other collection-related schemas,
    including creation and response models.

    Attributes:
        name (str): Human-readable name of the collection. Must contain
            between 1 and 100 characters.
        description (Optional[str]): Optional descriptive text providing
            additional information about the collection. Maximum length
            is 500 characters.

    Example:
        >>> collection = CollectionBase(
        ...     name="Example Collection",
        ...     description="A set of related prompts."
        ... )
        >>> collection.name
        'Example Collection'
    """
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class CollectionCreate(CollectionBase):
    """Schema used when creating a new collection.

    This model inherits all fields from CollectionBase and is typically
    used as the request body for API endpoints responsible for creating
    collections. System-managed fields such as identifiers and timestamps
    are not included in this schema.
    Attributes:
        name (str): Name of the collection to be created.
        description (Optional[str]): Optional description for the collection.
    Example:
        >>> payload = CollectionCreate(
        ...     name="Prompt Ideas",
        ...     description="Collection of creative writing prompts."
        ... )
        >>> payload.name
        'Prompt Ideas'
    """
    pass


class Collection(CollectionBase):
    """Represents a stored collection entity with metadata.

    This model extends CollectionBase by adding system-generated fields
    such as a unique identifier and creation timestamp. It is typically
    returned in API responses when retrieving or listing collections.

    Attributes:
        id (str): Unique identifier for the collection. Generated
            automatically using a UUID4 string.
        created_at (datetime): UTC timestamp indicating when the
            collection was created.

    Example:
        >>> collection = Collection(
        ...     name="Complete Collection"
        ... )
        >>> collection.id
        'generated-uuid'
        >>> isinstance(collection.created_at, datetime)
        True
    """
    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)

    model_config = ConfigDict(from_attributes=True)

# ============== Response Models ==============

class PromptList(BaseModel):
    """Represents a paginated or aggregated list of prompt resources.

    This response model is typically returned by API endpoints that list
    prompts. It contains the collection of prompt objects along with a
    total count representing the number of prompts available.
    Attributes:
        prompts (List[Prompt]): A list of prompt resources returned by the API.
        total (int): Total number of prompts available in the system or
            matching the applied query filters.

    Example:
        >>> prompt = Prompt(
        ...     title="Example Prompt",
        ...     content="Write a short story about space."
        ... )
        >>> response = PromptList(
        ...     prompts=[prompt],
        ...     total=1
        ... )
        >>> response.total
        1
    """

    prompts: List[Prompt]
    total: int

class CollectionList(BaseModel):
    """Represents a list of collection resources returned by the API.

    This model is used for endpoints that return multiple collections.
    It provides both the collection objects and a total count to help
    clients understand how many collections exist or match a query.
    Attributes:
        collections (List[Collection]): A list of collection objects
            returned by the API.
        total (int): Total number of collections available in the system
            or matching the applied query filters.
    Example:
        >>> collection = Collection(
        ...     name="Creative Prompts"
        ... )
        >>> response = CollectionList(
        ...     collections=[collection],
        ...     total=1
        ... )
        >>> response.collections[0].name
        'Creative Prompts'
    """

    collections: List[Collection]
    total: int


class HealthResponse(BaseModel):
    """Represents the health status of the PromptLab API.

    This response model is typically returned by a health-check endpoint
    and provides basic operational information about the running service,
    including its current status and version.

    Attributes:
        status (str): Current operational status of the application
            (e.g., "ok", "healthy", or "degraded").
        version (str): Version identifier of the running API service.

    Example:
        >>> health = HealthResponse(
        ...     status="healthy",
        ...     version="1.0.0"
        ... )
        >>> health.status
        'healthy'
    """
    status: str
    version: str
