"""API tests for PromptLab.

These tests verify API endpoint behavior including edge cases and
referential integrity rules.
"""

import time
from fastapi.testclient import TestClient


class TestHealth:
    """Tests for health endpoint."""

    def test_health_check(self, client: TestClient):
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()

        assert data["status"] == "healthy"
        assert "version" in data


class TestPrompts:
    """Tests for prompt endpoints."""

    def test_create_prompt(self, client: TestClient, sample_prompt_data):
        response = client.post("/prompts", json=sample_prompt_data)

        assert response.status_code == 201
        data = response.json()

        assert data["title"] == sample_prompt_data["title"]
        assert data["content"] == sample_prompt_data["content"]
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_create_prompt_invalid_collection(self, client: TestClient, sample_prompt_data):
        """Creating a prompt with non-existent collection should fail."""

        payload = {**sample_prompt_data, "collection_id": "invalid-id"}

        response = client.post("/prompts", json=payload)

        assert response.status_code == 404
        assert response.json()["detail"] == "Collection not found"

    def test_list_prompts_empty(self, client: TestClient):
        response = client.get("/prompts")

        assert response.status_code == 200
        data = response.json()

        assert data["prompts"] == []
        assert data["total"] == 0

    def test_list_prompts_with_data(self, client: TestClient, sample_prompt_data):
        client.post("/prompts", json=sample_prompt_data)

        response = client.get("/prompts")

        assert response.status_code == 200
        data = response.json()

        assert len(data["prompts"]) == 1
        assert data["total"] == 1

    def test_get_prompt_success(self, client: TestClient, sample_prompt_data):
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]

        response = client.get(f"/prompts/{prompt_id}")

        assert response.status_code == 200
        assert response.json()["id"] == prompt_id

    def test_get_prompt_not_found(self, client: TestClient):
        """Ensure non-existent prompt returns 404."""

        response = client.get("/prompts/nonexistent-id")

        assert response.status_code == 404
        assert response.json()["detail"] == "Prompt not found"

    def test_delete_prompt(self, client: TestClient, sample_prompt_data):
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]

        delete_response = client.delete(f"/prompts/{prompt_id}")

        assert delete_response.status_code == 204

        get_response = client.get(f"/prompts/{prompt_id}")
        assert get_response.status_code == 404

    def test_delete_prompt_not_found(self, client: TestClient):
        response = client.delete("/prompts/nonexistent-id")

        assert response.status_code == 404

    def test_update_prompt_put(self, client: TestClient, sample_prompt_data):
        """Full update should replace fields and update timestamp."""

        create_response = client.post("/prompts", json=sample_prompt_data)
        data = create_response.json()

        prompt_id = data["id"]
        original_updated_at = data["updated_at"]

        time.sleep(0.1)

        updated_data = {
            "title": "Updated Title",
            "content": "Updated content",
            "description": "Updated description"
        }

        response = client.put(f"/prompts/{prompt_id}", json=updated_data)

        assert response.status_code == 200
        updated = response.json()

        assert updated["title"] == "Updated Title"
        assert updated["content"] == "Updated content"
        assert updated["updated_at"] != original_updated_at

    def test_put_prompt_not_found(self, client: TestClient):
        payload = {
            "title": "Title",
            "content": "Content",
        }

        response = client.put("/prompts/nonexistent-id", json=payload)

        assert response.status_code == 404

    def test_patch_prompt_partial_update(self, client: TestClient, sample_prompt_data):
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]

        patch_payload = {"description": "New description"}

        response = client.patch(f"/prompts/{prompt_id}", json=patch_payload)

        assert response.status_code == 200
        data = response.json()

        assert data["description"] == "New description"
        assert data["title"] == sample_prompt_data["title"]

    def test_patch_prompt_not_found(self, client: TestClient):
        response = client.patch("/prompts/nonexistent-id", json={"title": "Test"})

        assert response.status_code == 404

    def test_sorting_order_newest_first(self, client: TestClient):
        """Prompts should be returned newest first."""

        prompt1 = {"title": "First", "content": "First prompt"}
        prompt2 = {"title": "Second", "content": "Second prompt"}

        client.post("/prompts", json=prompt1)
        time.sleep(0.1)
        client.post("/prompts", json=prompt2)

        response = client.get("/prompts")
        prompts = response.json()["prompts"]

        assert prompts[0]["title"] == "Second"
        assert prompts[1]["title"] == "First"

    def test_filter_prompts_by_collection(self, client: TestClient, sample_collection_data):
        """Verify prompts can be filtered by collection."""

        col_resp = client.post("/collections", json=sample_collection_data)
        collection_id = col_resp.json()["id"]

        client.post(
            "/prompts",
            json={
                "title": "In Collection",
                "content": "Content",
                "collection_id": collection_id
            },
        )

        client.post(
            "/prompts",
            json={"title": "No Collection", "content": "Other"},
        )

        response = client.get(f"/prompts?collection_id={collection_id}")

        data = response.json()

        assert data["total"] == 1
        assert data["prompts"][0]["collection_id"] == collection_id

    def test_search_prompts(self, client: TestClient):
        """Search should match prompt title or content."""

        client.post(
            "/prompts",
            json={"title": "AI Prompt", "content": "Artificial intelligence"},
        )

        client.post(
            "/prompts",
            json={"title": "Cooking Prompt", "content": "Food recipe"},
        )

        response = client.get("/prompts?search=AI")

        data = response.json()

        assert data["total"] == 1
        assert data["prompts"][0]["title"] == "AI Prompt"


class TestPromptValidation:
    """Validation and schema behavior tests."""

    def test_create_prompt_missing_required_fields(self, client: TestClient):
        """Missing required fields should trigger FastAPI validation."""

        response = client.post("/prompts", json={"title": "Incomplete"})

        assert response.status_code == 422

    def test_create_prompt_empty_title_validation(self, client: TestClient):
        """Ensure empty title is rejected if validation rules exist."""

        payload = {
            "title": "",
            "content": "Content with empty title"
        }

        response = client.post("/prompts", json=payload)

        # Either schema validation or business validation should fail
        assert response.status_code in [400, 422]


class TestPromptFilteringCombinations:
    """Tests combining multiple query filters."""

    def test_filter_by_collection_and_search(self, client: TestClient, sample_collection_data):
        """Ensure filters work together correctly."""

        col_resp = client.post("/collections", json=sample_collection_data)
        collection_id = col_resp.json()["id"]

        client.post(
            "/prompts",
            json={
                "title": "AI Prompt",
                "content": "Artificial intelligence",
                "collection_id": collection_id,
            },
        )

        client.post(
            "/prompts",
            json={
                "title": "Cooking Prompt",
                "content": "Recipe content",
                "collection_id": collection_id,
            },
        )

        response = client.get(
            f"/prompts?collection_id={collection_id}&search=AI"
        )

        data = response.json()

        assert response.status_code == 200
        assert data["total"] == 1
        assert data["prompts"][0]["title"] == "AI Prompt"

class TestPromptUpdateIntegrity:
    """Ensure updates preserve immutable fields."""

    def test_patch_prompt_preserves_created_at(self, client: TestClient, sample_prompt_data):
        """created_at should never change after updates."""

        create_resp = client.post("/prompts", json=sample_prompt_data)
        prompt = create_resp.json()

        prompt_id = prompt["id"]
        original_created_at = prompt["created_at"]

        time.sleep(0.1)

        patch_resp = client.patch(
            f"/prompts/{prompt_id}",
            json={"title": "Changed"}
        )

        updated = patch_resp.json()

        assert updated["created_at"] == original_created_at
        assert updated["updated_at"] != prompt["updated_at"]

class TestPromptListConsistency:
    """API contract tests for list endpoints."""

    def test_list_prompts_total_matches_length(self, client: TestClient):
        """Ensure `total` field always matches actual list length."""

        client.post("/prompts", json={"title": "A", "content": "A"})
        client.post("/prompts", json={"title": "B", "content": "B"})

        response = client.get("/prompts")
        data = response.json()

        assert data["total"] == len(data["prompts"])


class TestCollections:
    """Tests for collection endpoints."""

    def test_create_collection(self, client: TestClient, sample_collection_data):
        response = client.post("/collections", json=sample_collection_data)

        assert response.status_code == 201
        data = response.json()

        assert data["name"] == sample_collection_data["name"]
        assert "id" in data

    def test_list_collections(self, client: TestClient, sample_collection_data):
        client.post("/collections", json=sample_collection_data)

        response = client.get("/collections")

        assert response.status_code == 200
        data = response.json()

        assert len(data["collections"]) == 1
        assert data["total"] == 1

    def test_get_collection_success(self, client: TestClient, sample_collection_data):
        create_resp = client.post("/collections", json=sample_collection_data)
        collection_id = create_resp.json()["id"]

        response = client.get(f"/collections/{collection_id}")

        assert response.status_code == 200
        assert response.json()["id"] == collection_id

    def test_get_collection_not_found(self, client: TestClient):
        response = client.get("/collections/nonexistent-id")

        assert response.status_code == 404

    def test_delete_collection(self, client: TestClient, sample_collection_data):
        create_resp = client.post("/collections", json=sample_collection_data)
        collection_id = create_resp.json()["id"]

        delete_resp = client.delete(f"/collections/{collection_id}")

        assert delete_resp.status_code == 204

        get_resp = client.get(f"/collections/{collection_id}")
        assert get_resp.status_code == 404

    def test_delete_collection_removes_associated_prompts(
        self, client: TestClient, sample_collection_data
    ):
        """Deleting a collection should remove its prompts."""

        col_resp = client.post("/collections", json=sample_collection_data)
        collection_id = col_resp.json()["id"]

        prompt_resp = client.post(
            "/prompts",
            json={
                "title": "Linked Prompt",
                "content": "Content",
                "collection_id": collection_id,
            },
        )

        prompt_id = prompt_resp.json()["id"]

        client.delete(f"/collections/{collection_id}")

        get_prompt = client.get(f"/prompts/{prompt_id}")

        assert get_prompt.status_code == 404


class TestCollectionIntegrity:
    """Collection relationship integrity tests."""

    def test_create_prompt_after_collection_deleted(self, client: TestClient, sample_collection_data):
        """Creating prompt referencing deleted collection should fail."""

        col_resp = client.post("/collections", json=sample_collection_data)
        collection_id = col_resp.json()["id"]

        client.delete(f"/collections/{collection_id}")

        response = client.post(
            "/prompts",
            json={
                "title": "Should Fail",
                "content": "Invalid reference",
                "collection_id": collection_id,
            },
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Collection not found"