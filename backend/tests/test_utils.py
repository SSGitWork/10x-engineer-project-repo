"""Unit tests for utility functions in utils.py."""

import pytest
from datetime import datetime, timedelta
from types import SimpleNamespace

from app.utils import (
    sort_prompts_by_date,
    filter_prompts_by_collection,
    search_prompts,
    normalize_tags,
    parse_tags_query,
    filter_prompts_by_tags,
    validate_prompt_content,
    extract_variables,
)


def make_prompt(**kwargs):
    """Helper to create a lightweight Prompt-like object."""
    defaults = {
        "id": "p1",
        "title": "Title",
        "description": None,
        "collection_id": None,
        "tags": [],
        "created_at": datetime.utcnow(),
    }
    defaults.update(kwargs)
    return SimpleNamespace(**defaults)


class TestSortPrompts:
    def test_sort_prompts_descending(self):
        now = datetime.utcnow()

        p1 = make_prompt(title="Old", created_at=now - timedelta(days=1))
        p2 = make_prompt(title="New", created_at=now)

        result = sort_prompts_by_date([p1, p2])

        assert result[0].title == "New"
        assert result[1].title == "Old"

    def test_sort_prompts_ascending(self):
        now = datetime.utcnow()

        p1 = make_prompt(title="Old", created_at=now - timedelta(days=1))
        p2 = make_prompt(title="New", created_at=now)

        result = sort_prompts_by_date([p1, p2], descending=False)

        assert result[0].title == "Old"
        assert result[1].title == "New"

    def test_sort_empty_list(self):
        assert sort_prompts_by_date([]) == []


class TestFilterByCollection:
    def test_filter_prompts_by_collection_match(self):
        p1 = make_prompt(collection_id="col1")
        p2 = make_prompt(collection_id="col2")

        result = filter_prompts_by_collection([p1, p2], "col1")

        assert len(result) == 1
        assert result[0].collection_id == "col1"

    def test_filter_prompts_by_collection_no_match(self):
        p1 = make_prompt(collection_id="col1")

        result = filter_prompts_by_collection([p1], "col2")

        assert result == []


class TestSearchPrompts:
    def test_search_matches_title(self):
        p1 = make_prompt(title="AI Prompt")
        p2 = make_prompt(title="Cooking Prompt")

        results = search_prompts([p1, p2], "ai")

        assert len(results) == 1
        assert results[0].title == "AI Prompt"

    def test_search_matches_description(self):
        p1 = make_prompt(description="Machine learning prompt")
        p2 = make_prompt(description="Cooking tips")

        results = search_prompts([p1, p2], "learning")

        assert len(results) == 1

    def test_search_case_insensitive(self):
        p1 = make_prompt(title="Hello World")

        results = search_prompts([p1], "hello")

        assert len(results) == 1

    def test_search_no_results(self):
        p1 = make_prompt(title="Hello")

        results = search_prompts([p1], "xyz")

        assert results == []


class TestNormalizeTags:
    def test_normalize_tags_lowercase_and_trim(self):
        tags = [" AI ", "ML"]

        result = normalize_tags(tags)

        assert result == ["ai", "ml"]

    def test_normalize_tags_remove_duplicates(self):
        tags = ["ai", "AI", "ml"]

        result = normalize_tags(tags)

        assert set(result) == {"ai", "ml"}

    def test_normalize_tags_empty(self):
        assert normalize_tags([]) == []

    def test_normalize_tags_none(self):
        assert normalize_tags(None) == []

    def test_tag_length_validation(self):
        long_tag = "a" * 51

        with pytest.raises(ValueError):
            normalize_tags([long_tag])

    def test_tag_character_validation(self):
        with pytest.raises(ValueError):
            normalize_tags(["invalid-tag!"])


class TestParseTagsQuery:
    def test_parse_tags_query_basic(self):
        result = parse_tags_query("ai,ml")

        assert result == ["ai", "ml"]

    def test_parse_tags_query_trimming(self):
        result = parse_tags_query(" ai , ml ")

        assert result == ["ai", "ml"]

    def test_parse_tags_query_empty_values(self):
        result = parse_tags_query("ai,,ml")

        assert result == ["ai", "ml"]


class TestFilterPromptsByTags:
    def test_filter_prompts_by_single_tag(self):
        p1 = make_prompt(tags=["ai"])
        p2 = make_prompt(tags=["ml"])

        result = filter_prompts_by_tags([p1, p2], ["ai"])

        assert len(result) == 1
        assert result[0].tags == ["ai"]

    def test_filter_prompts_by_multiple_tags(self):
        p1 = make_prompt(tags=["ai"])
        p2 = make_prompt(tags=["ml"])

        result = filter_prompts_by_tags([p1, p2], ["ai", "ml"])

        assert len(result) == 2

    def test_filter_prompts_no_match(self):
        p1 = make_prompt(tags=["ai"])

        result = filter_prompts_by_tags([p1], ["ml"])

        assert result == []

    def test_filter_prompts_handles_empty_tags(self):
        p1 = make_prompt(tags=[])

        result = filter_prompts_by_tags([p1], ["ai"])

        assert result == []


class TestValidatePromptContent:
    def test_valid_prompt_content(self):
        assert validate_prompt_content("This is a valid prompt")

    def test_prompt_content_whitespace(self):
        assert not validate_prompt_content("   ")

    def test_prompt_content_too_short(self):
        assert not validate_prompt_content("short")

    def test_prompt_content_none(self):
        assert not validate_prompt_content(None)


class TestExtractVariables:
    def test_extract_single_variable(self):
        result = extract_variables("Hello {{name}}")

        assert result == ["name"]

    def test_extract_multiple_variables(self):
        result = extract_variables("Hello {{name}} from {{city}}")

        assert set(result) == {"name", "city"}

    def test_extract_no_variables(self):
        result = extract_variables("Hello world")

        assert result == []

    def test_extract_duplicate_variables(self):
        result = extract_variables("{{name}} and {{name}}")

        assert result == ["name", "name"]