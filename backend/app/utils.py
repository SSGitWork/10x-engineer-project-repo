"""Utility functions for PromptLab"""

from typing import List
# To avoid circular dependency
# models -> utils
# utils -> models
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models import Prompt
    
import re

def sort_prompts_by_date(prompts: List[Prompt], descending: bool = True) -> List[Prompt]:
    """Sort prompts by their creation date.

    Args:
        prompts (List[Prompt]): The list of prompts to be sorted.
        descending (bool, optional): If True, sorts by newest to oldest. Defaults to True.

    Returns:
        List[Prompt]: The list of prompts sorted by creation date.

    Example:
        >>> prompts = [Prompt(name="A", created_at="2023-01-01"),
        ...            Prompt(name="B", created_at="2023-02-01")]
        >>> sorted_prompts = sort_prompts_by_date(prompts)
        >>> sorted_prompts[0].name
        'B'
    """
    return sorted(prompts, key=lambda p: p.created_at, reverse=descending)

def filter_prompts_by_collection(prompts: List[Prompt], collection_id: str) -> List[Prompt]:
    """Filter prompts by collection ID.

    Args:
        prompts (List[Prompt]): The list of prompts to filter.
        collection_id (str): The collection ID to filter by.

    Returns:
        List[Prompt]: Prompts that belong to the specified collection.

    Example:
        >>> prompts = [Prompt(name="A", collection_id="col-1"),
        ...            Prompt(name="B", collection_id="col-2")]
        >>> filtered_prompts = filter_prompts_by_collection(prompts, "col-1")
        >>> filtered_prompts[0].name
        'A'
    """
    return [p for p in prompts if p.collection_id == collection_id]

def search_prompts(prompts: List[Prompt], query: str) -> List[Prompt]:
    """Search prompts containing the query in the title or description.

    Args:
        prompts (List[Prompt]): The list of prompts to search within.
        query (str): The search query string.

    Returns:
        List[Prompt]: Prompts that contain the query in their title or description.

    Example:
        >>> prompts = [Prompt(name="A", title="Welcome"),
        ...            Prompt(name="B", title="Hello World")]
        >>> results = search_prompts(prompts, "hello")
        >>> results[0].title
        'Hello World'
    """
    query_lower = query.lower()
    return [
        p for p in prompts
        if query_lower in p.title.lower() or
           (p.description and query_lower in p.description.lower())
    ]

def normalize_tags(tags: List[str]) -> List[str]:
    """Normalize and validate tags.

    - trims whitespace
    - converts to lowercase
    - removes duplicates
    - validates length and characters
    """
    if tags is None:
        return []

    cleaned = []
    seen = set()

    for tag in tags:
        tag = tag.strip().lower()

        if len(tag) > 50:
            raise ValueError("Tag length exceeds 50 characters")

        if not re.match(r"^[a-z0-9 ]+$", tag):
            raise ValueError("Tags must be alphanumeric and may contain spaces")

        if tag not in seen:
            cleaned.append(tag)
            seen.add(tag)

    return cleaned


def parse_tags_query(tags: str) -> List[str]:
    """Parse comma-separated tag query parameter."""
    return normalize_tags([t.strip() for t in tags.split(",") if t.strip()])


def filter_prompts_by_tags(prompts: List[Prompt], tags: List[str]) -> List[Prompt]:
    """Filter prompts that match ANY of the provided tags.

    Args:
        prompts (List[Prompt]): The list of prompts.
        tags (List[str]): Tags to filter by.

    Returns:
        List[Prompt]: Prompts containing any of the provided tags.
    """
    tag_set = set(tags)

    return [
        p for p in prompts
        if p.tags and tag_set.intersection(set(p.tags))
    ]


def validate_prompt_content(content: str) -> bool:
    """Check if prompt content is valid.

    A valid prompt should:
    - Not be empty
    - Not be just whitespace
    - Be at least 10 characters

    Args:
        content (str): The content of the prompt to validate.

    Returns:
        bool: True if valid, otherwise False.

    Example:
        >>> validate_prompt_content("Hello World")
        True
        >>> validate_prompt_content("   ")
        False
    """
    if not content or not content.strip():
        return False
    return len(content.strip()) >= 10

def extract_variables(content: str) -> List[str]:
    """Extract template variables from prompt content.

    Variables are identified within double curly braces, e.g., {{variable_name}}.

    Args:
        content (str): The content string to extract variables from.

    Returns:
        List[str]: A list of variable names found within the content.

    Example:
        >>> extract_variables("Hello {{name}}, welcome to {{place}}!")
        ['name', 'place']
    """
    import re
    pattern = r'\{\{(\w+)\}\}'
    return re.findall(pattern, content)
