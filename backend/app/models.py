"""Pydantic models for PromptLab"""

from datetime import datetime, UTC
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator, ConfigDict
from uuid import uuid4
from app.utils import normalize_tags

def generate_id() -> str:
    """Generate a unique identifier using UUID4.

    Returns:
        str: A new unique identifier as a string.

    Example:
        >>> generate_id()
        'a8098c1a-f86e-11da-bd1a-00112444be1e'
    """
    return str(uuid4())

def get_current_time() -> datetime:
    """Get the current UTC datetime.

    Returns:
        datetime: The current datetime in UTC.

    Example:
        >>> get_current_time()
        datetime.datetime(2023, 10, 3, 12, 34, 56, 789012)
    """
    return datetime.now(UTC)

# ============== Prompt Models ==============

class PromptBase(BaseModel):
    """Base model for defining prompt attributes.

    Attributes:
        title (str): The title of the prompt, must be between 1 and 200 characters.
        content (str): The content of the prompt, must have at least 1 character.
        description (Optional[str]): Optional description of the prompt, up to 500 characters.
        collection_id (Optional[str]): Identifier of the associated collection, if any.

    Example:
        >>> prompt = PromptBase(
        ...     title="Example Prompt",
        ...     content="This is the prompt content.",
        ...     description="An optional description."
        ... )
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
    """Model for creating a new prompt based on PromptBase attributes.

    Inherits all attributes from PromptBase.

    Example:
        >>> prompt_create = PromptCreate(
        ...     title="Create Prompt",
        ...     content="Prompt content for creation."
        ... )
    """
    pass

class PromptUpdate(BaseModel):
    """Model for partially updating a prompt.

    All fields are optional. Only provided fields will be updated.
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
    """Model representing a complete prompt with metadata attributes.

    Inherits all attributes from PromptBase, and adds unique identifiers and timestamps.

    Attributes:
        id (str): Unique identifier for the prompt.
        created_at (datetime): Timestamp of when the prompt was created.
        updated_at (datetime): Timestamp of when the prompt was last updated.

    Example:
        >>> prompt = Prompt(
        ...     title="Final Prompt",
        ...     content="Complete prompt content.",
        ...     id="123"
        ... )
    """
    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)
    updated_at: datetime = Field(default_factory=get_current_time)

    model_config = ConfigDict(from_attributes=True)

# ============== Collection Models ==============

class CollectionBase(BaseModel):
    """Base model for defining collection attributes.

    Attributes:
        name (str): The name of the collection, requires 1 to 100 characters.
        description (Optional[str]): Optional description about the collection, up to 500 characters.

    Example:
        >>> collection = CollectionBase(
        ...     name="Example Collection",
        ...     description="An optional collection description."
        ... )
    """
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)

class CollectionCreate(CollectionBase):
    """Model for creating a new collection using CollectionBase attributes.

    Inherits all attributes from CollectionBase.

    Example:
        >>> collection_create = CollectionCreate(
        ...     name="New Collection"
        ... )
    """
    pass

class Collection(CollectionBase):
    """Model representing a full collection entity with metadata.

    Inherits all attributes from CollectionBase, adding unique identifiers and timestamps.

    Attributes:
        id (str): Unique identifier for the collection.
        created_at (datetime): Timestamp of when the collection was created.

    Example:
        >>> collection = Collection(
        ...     name="Complete Collection",
        ...     id="456"
        ... )
    """
    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)

    model_config = ConfigDict(from_attributes=True)

# ============== Response Models ==============

class PromptList(BaseModel):
    """Model representing a list of prompts in a response.

    Attributes:
        prompts (List[Prompt]): List of Prompt objects.
        total (int): Total number of prompts available.

    Example:
        >>> prompt_list = PromptList(
        ...     prompts=[Prompt(title="Sample", content="Content", id="123")],
        ...     total=1
        ... )
    """
    prompts: List[Prompt]
    total: int

class CollectionList(BaseModel):
    """Model representing a list of collections in a response.

    Attributes:
        collections (List[Collection]): List of Collection objects.
        total (int): Total number of collections available.

    Example:
        >>> collection_list = CollectionList(
        ...     collections=[Collection(name="Sample Collection", id="456")],
        ...     total=1
        ... )
    """
    collections: List[Collection]
    total: int

class HealthResponse(BaseModel):
    """Model for the health status response of the API.

    Attributes:
        status (str): The current health status of the application.
        version (str): The current version of the application.

    Example:
        >>> health = HealthResponse(
        ...     status="Healthy",
        ...     version="1.0.0"
        ... )
    """
    status: str
    version: str
