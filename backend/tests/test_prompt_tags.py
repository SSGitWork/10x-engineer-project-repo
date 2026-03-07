"""Tests for Prompt tagging system (TDD Red phase).

These tests define the expected behavior of the tagging feature.
Initial scaffolding exists but functionality is not implemented yet,
so several tests are expected to fail.
"""

from fastapi.testclient import TestClient


def create_collection(client: TestClient):
    """Helper to create a collection for prompt tests."""
    response = client.post(
        "/collections",
        json={"name": "Test Collection", "description": "Test"}
    )
    assert response.status_code == 201
    return response.json()["id"]


def test_create_prompt_with_tags_success(client: TestClient):
    collection_id = create_collection(client)

    payload = {
        "title": "Tagged Prompt",
        "content": "Example content for tagging",
        "collection_id": collection_id,
        "tags": ["ai", "ml"]
    }

    response = client.post("/prompts", json=payload)

    assert response.status_code == 201
    data = response.json()

    assert "tags" in data
    assert set(data["tags"]) == {"ai", "ml"}


def test_create_prompt_without_tags(client: TestClient):
    collection_id = create_collection(client)

    payload = {
        "title": "No Tags",
        "content": "Prompt without tags",
        "collection_id": collection_id
    }

    response = client.post("/prompts", json=payload)

    assert response.status_code == 201
    data = response.json()

    assert "tags" in data
    assert data["tags"] == []


def test_create_prompt_normalizes_tags(client: TestClient):
    collection_id = create_collection(client)

    payload = {
        "title": "Normalize Tags",
        "content": "Testing normalization",
        "collection_id": collection_id,
        "tags": ["AI", "Machine Learning"]
    }

    response = client.post("/prompts", json=payload)

    assert response.status_code == 201
    data = response.json()

    # Expect lowercase normalization
    assert "ai" in data["tags"]
    assert "machine learning" in data["tags"]


def test_create_prompt_removes_duplicate_tags(client: TestClient):
    collection_id = create_collection(client)

    payload = {
        "title": "Duplicate Tags",
        "content": "Testing duplicates",
        "collection_id": collection_id,
        "tags": ["ai", "ai", "ml"]
    }

    response = client.post("/prompts", json=payload)

    assert response.status_code == 201
    data = response.json()

    assert len(data["tags"]) == 2
    assert set(data["tags"]) == {"ai", "ml"}


def test_reject_tag_longer_than_50_characters(client: TestClient):
    collection_id = create_collection(client)

    long_tag = "a" * 51

    payload = {
        "title": "Invalid Tag",
        "content": "Testing long tag validation",
        "collection_id": collection_id,
        "tags": [long_tag]
    }

    response = client.post("/prompts", json=payload)

    assert response.status_code == 422


def test_patch_prompt_updates_tags(client: TestClient):
    collection_id = create_collection(client)

    create_payload = {
        "title": "Patch Tags",
        "content": "Initial content",
        "collection_id": collection_id
    }

    create_resp = client.post("/prompts", json=create_payload)
    prompt_id = create_resp.json()["id"]

    patch_resp = client.patch(
        f"/prompts/{prompt_id}",
        json={"tags": ["ai", "testing"]}
    )

    assert patch_resp.status_code == 200
    data = patch_resp.json()

    assert set(data["tags"]) == {"ai", "testing"}


def test_patch_prompt_removes_tags(client: TestClient):
    collection_id = create_collection(client)

    create_payload = {
        "title": "Remove Tags",
        "content": "Initial content",
        "collection_id": collection_id,
        "tags": ["ai", "ml"]
    }

    create_resp = client.post("/prompts", json=create_payload)
    prompt_id = create_resp.json()["id"]

    patch_resp = client.patch(
        f"/prompts/{prompt_id}",
        json={"tags": []}
    )

    assert patch_resp.status_code == 200
    data = patch_resp.json()

    assert data["tags"] == []


def test_filter_prompts_by_single_tag(client: TestClient):
    collection_id = create_collection(client)

    client.post(
        "/prompts",
        json={
            "title": "AI Prompt",
            "content": "AI content",
            "collection_id": collection_id,
            "tags": ["ai"]
        },
    )

    client.post(
        "/prompts",
        json={
            "title": "ML Prompt",
            "content": "ML content",
            "collection_id": collection_id,
            "tags": ["ml"]
        },
    )

    response = client.get("/prompts?tags=ai")

    assert response.status_code == 200
    data = response.json()

    assert data["total"] == 1
    assert data["prompts"][0]["title"] == "AI Prompt"


def test_filter_prompts_by_multiple_tags(client: TestClient):
    collection_id = create_collection(client)

    client.post(
        "/prompts",
        json={
            "title": "AI Prompt",
            "content": "AI content",
            "collection_id": collection_id,
            "tags": ["ai"]
        },
    )

    client.post(
        "/prompts",
        json={
            "title": "ML Prompt",
            "content": "ML content",
            "collection_id": collection_id,
            "tags": ["ml"]
        },
    )

    response = client.get("/prompts?tags=ai,ml")

    assert response.status_code == 200
    data = response.json()

    assert data["total"] == 2


def test_filter_prompts_returns_empty(client: TestClient):
    collection_id = create_collection(client)

    client.post(
        "/prompts",
        json={
            "title": "Prompt",
            "content": "Some content",
            "collection_id": collection_id,
            "tags": ["ai"]
        },
    )

    response = client.get("/prompts?tags=nonexistent")

    assert response.status_code == 200
    data = response.json()

    assert data["total"] == 0
    assert data["prompts"] == []