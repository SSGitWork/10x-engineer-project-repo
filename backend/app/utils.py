"""Utility functions for PromptLab"""
from typing import List, Optional
import re

# !NOTE: A interim measure 
# to avoid circular dependency between models.py & utils.py 
class Prompt:
    pass

def sort_prompts_by_date(prompts: List[Prompt], descending: bool = True) -> List[Prompt]:
    """Sort prompts by their creation timestamp.

    This utility orders a list of Prompt objects based on their ``created_at``
    attribute. By default, prompts are returned from newest to oldest, but the
    order can be reversed by setting ``descending`` to False.

    Args:
        prompts (List[Prompt]): A list of Prompt objects to be sorted.
        descending (bool): If True, sort from newest to oldest. If False,
            sort from oldest to newest. Defaults to True.

    Returns:
        List[Prompt]: A new list of Prompt objects sorted by the ``created_at``
        attribute.

    Example:
        >>> prompts = [
        ...     Prompt(name="A", created_at="2023-01-01"),
        ...     Prompt(name="B", created_at="2023-02-01"),
        ... ]
        >>> sorted_prompts = sort_prompts_by_date(prompts)
        >>> sorted_prompts[0].name
        'B'
    """
    return sorted(prompts, key=lambda p: p.created_at, reverse=descending)


def filter_prompts_by_collection(prompts: List[Prompt], collection_id: str) -> List[Prompt]:
    """Filter prompts belonging to a specific collection.

    This helper returns only the prompts whose ``collection_id`` matches
    the provided identifier.

    Args:
        prompts (List[Prompt]): A list of Prompt objects to filter.
        collection_id (str): The identifier of the collection to match.

    Returns:
        List[Prompt]: A list of Prompt objects that belong to the specified
        collection.

    Example:
        >>> prompts = [
        ...     Prompt(name="A", collection_id="col-1"),
        ...     Prompt(name="B", collection_id="col-2"),
        ... ]
        >>> filtered_prompts = filter_prompts_by_collection(prompts, "col-1")
        >>> filtered_prompts[0].name
        'A'
    """
    return [p for p in prompts if p.collection_id == collection_id]


def search_prompts(prompts: List[Prompt], query: str) -> List[Prompt]:
    """Search prompts by a text query.

    Performs a case-insensitive search across the ``title`` and
    ``description`` fields of each Prompt. A prompt is included in the
    results if the query appears in either field.
    Args:
        prompts (List[Prompt]): A list of Prompt objects to search through.
        query (str): The search string used to match against prompt titles
            and descriptions.

    Returns:
        List[Prompt]: A list of Prompt objects whose title or description
        contains the query string.

    Example:
        >>> prompts = [
        ...     Prompt(name="A", title="Welcome"),
        ...     Prompt(name="B", title="Hello World"),
        ... ]
        >>> results = search_prompts(prompts, "hello")
        >>> results[0].title
        'Hello World'
    """
    query_lower = query.lower()
    return [
        p for p in prompts
        if query_lower in p.title.lower()
        or (p.description and query_lower in p.description.lower())
    ]

def normalize_tags(tags: List[str]) -> List[str]:
    """Normalize and validate a list of tags.

    This utility cleans and validates tag values to ensure consistency across
    the application. Each tag is stripped of surrounding whitespace, converted
    to lowercase, validated for allowed characters, and deduplicated while
    preserving order.

    Validation rules:
    - Tags must contain only lowercase letters, numbers, and spaces.
    - Tags must not exceed 50 characters.
    - Duplicate tags are removed.
    Args:
        tags (List[str]): A list of raw tag strings that may contain mixed
            casing, extra whitespace, or duplicates.
    Returns:
        List[str]: A normalized list of unique tags that conform to the
        validation rules.

    Raises:
        ValueError: If a tag exceeds 50 characters or contains invalid
        characters.

    Example:
        >>> normalize_tags(["  AI ", "Machine Learning", "ai"])
        ['ai', 'machine learning']
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
    """Parse a comma-separated tag query string into normalized tags.

    This helper converts a query parameter string into a validated list
    of normalized tags. Each tag is trimmed, filtered for emptiness,
    and then passed through ``normalize_tags`` for validation and cleanup.

    Args:
        tags (str): A comma-separated string of tags provided in a query
            parameter (e.g., "ai, writing, prompts").

    Returns:
        List[str]: A normalized list of validated tag strings.

    Raises:
        ValueError: If any tag fails validation during normalization.

    Example:
        >>> parse_tags_query("AI, Writing, prompts")
        ['ai', 'writing', 'prompts']
    """
    return normalize_tags([t.strip() for t in tags.split(",") if t.strip()])


def filter_prompts_by_tags(prompts: List[Prompt], tags: List[str]) -> List[Prompt]:
    """Filter prompts that contain any of the specified tags.

    This function returns prompts whose ``tags`` field shares at least
    one tag with the provided list. The match is performed using set
    intersection for efficiency.

    Args:
        prompts (List[Prompt]): The list of Prompt objects to filter.
        tags (List[str]): A list of tags used as filter criteria.

    Returns:
        List[Prompt]: A list of prompts containing at least one of the
        specified tags.

    Example:
        >>> prompts = [
        ...     Prompt(name="A", tags=["ai", "writing"]),
        ...     Prompt(name="B", tags=["marketing"]),
        ... ]
        >>> results = filter_prompts_by_tags(prompts, ["ai"])
        >>> results[0].name
        'A'
    """
    tag_set = set(tags)

    return [
        p for p in prompts
        if p.tags and tag_set.intersection(set(p.tags))
    ]


def query_prompts(
    prompts: List[Prompt],
    collection_id: Optional[str] = None,
    search: Optional[str] = None,
    tags: Optional[List[str]] = None
) -> List[Prompt]:
    """Apply collection, search, and tag filters to a list of prompts.

    This utility processes a list of Prompt objects by optionally applying
    a collection filter, a text search, and a tag-based filter. The resulting
    prompts are then sorted by their creation timestamp in descending order
    (newest first).

    Args:
        prompts (List[Prompt]): The base list of Prompt objects to process.
        collection_id (Optional[str]): Identifier of the collection used to
            filter prompts. If provided, only prompts belonging to this
            collection are included.
        search (Optional[str]): A case-insensitive search query applied to
            prompt titles and descriptions.
        tags (Optional[List[str]]): A list of normalized tags used to filter
            prompts. Prompts containing at least one matching tag are included.

    Returns:
        List[Prompt]: A list of prompts filtered according to the provided
        criteria and sorted by ``created_at`` from newest to oldest.
    Example:
        >>> results = query_prompts(
        ...     prompts=all_prompts,
        ...     collection_id="col-123",
        ...     search="welcome",
        ...     tags=["ai", "writing"]
        ... )
        >>> len(results) >= 0
        True
    """
    results = prompts

    if collection_id:
        results = filter_prompts_by_collection(results, collection_id)

    if search:
        results = search_prompts(results, search)

    if tags:
        results = filter_prompts_by_tags(results, tags)

    return sort_prompts_by_date(results, descending=True)


def validate_prompt_content(content: str) -> bool:
    """Validate the textual content of a prompt.

    This helper checks whether a prompt's content meets basic validity rules.
    A valid prompt must contain non-whitespace characters and must be at
    least 10 characters long after trimming leading and trailing whitespace.
    Args:
        content (str): The prompt content string to validate.

    Returns:
        bool: True if the content is non-empty and contains at least
        10 non-whitespace characters, otherwise False.
    Example:
        >>> validate_prompt_content("Write a short poem about the sea.")
        True
        >>> validate_prompt_content("   ")
        False
    """
    if not content or not content.strip():
        return False
    return len(content.strip()) >= 10


def extract_variables(content: str) -> List[str]:
    """Extract template variables from prompt content.

    Variables are detected using the double-curly-brace syntax
    ``{{variable_name}}`` commonly used in prompt templates. The function
    returns all variable names found in the content string.

    Args:
        content (str): The prompt content containing potential template
            variables.

    Returns:
        List[str]: A list of variable names extracted from the content.
        If no variables are present, an empty list is returned.

    Example:
        >>> extract_variables("Hello {{name}}, welcome to {{place}}!")
        ['name', 'place']
    """
    pattern = r'\{\{(\w+)\}\}'
    return re.findall(pattern, content)