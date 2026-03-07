"""Unit tests for the Storage class."""

from app.storage import Storage
from app.models import Prompt, Collection


class TestPromptStorage:
    """Tests for prompt-related storage operations."""

    def test_create_and_get_prompt(self):
        storage = Storage()

        prompt = Prompt(title="Test", content="Content")
        storage.create_prompt(prompt)

        result = storage.get_prompt(prompt.id)

        assert result is not None
        assert result.id == prompt.id
        assert result.title == "Test"

    def test_get_all_prompts(self):
        storage = Storage()

        p1 = Prompt(title="A", content="A")
        p2 = Prompt(title="B", content="B")

        storage.create_prompt(p1)
        storage.create_prompt(p2)

        prompts = storage.get_all_prompts()

        assert len(prompts) == 2

    def test_update_prompt_success(self):
        storage = Storage()

        prompt = Prompt(title="Old", content="Old")
        storage.create_prompt(prompt)

        updated = Prompt(
            id=prompt.id,
            title="New",
            content="New",
            description=None,
            collection_id=None,
            tags=[],
            created_at=prompt.created_at,
            updated_at=prompt.updated_at,
        )

        result = storage.update_prompt(prompt.id, updated)

        assert result is not None
        assert result.title == "New"

    def test_update_prompt_not_found(self):
        storage = Storage()

        prompt = Prompt(title="Test", content="Content")

        result = storage.update_prompt("missing-id", prompt)

        assert result is None

    def test_delete_prompt_success(self):
        storage = Storage()

        prompt = Prompt(title="Test", content="Content")
        storage.create_prompt(prompt)

        result = storage.delete_prompt(prompt.id)

        assert result is True
        assert storage.get_prompt(prompt.id) is None

    def test_delete_prompt_not_found(self):
        storage = Storage()

        result = storage.delete_prompt("missing-id")

        assert result is False


class TestCollectionStorage:
    """Tests for collection-related storage operations."""

    def test_create_and_get_collection(self):
        storage = Storage()

        collection = Collection(name="Test Collection")
        storage.create_collection(collection)

        result = storage.get_collection(collection.id)

        assert result is not None
        assert result.id == collection.id

    def test_get_all_collections(self):
        storage = Storage()

        c1 = Collection(name="A")
        c2 = Collection(name="B")

        storage.create_collection(c1)
        storage.create_collection(c2)

        collections = storage.get_all_collections()

        assert len(collections) == 2

    def test_collection_exists_true(self):
        storage = Storage()

        col = Collection(name="Test")
        storage.create_collection(col)

        assert storage.collection_exists(col.id) is True

    def test_collection_exists_false(self):
        storage = Storage()

        assert storage.collection_exists("missing-id") is False

    def test_delete_collection_success(self):
        storage = Storage()

        col = Collection(name="Test")
        storage.create_collection(col)

        result = storage.delete_collection(col.id)

        assert result is True
        assert storage.get_collection(col.id) is None

    def test_delete_collection_not_found(self):
        storage = Storage()

        result = storage.delete_collection("missing-id")

        assert result is False


class TestCollectionPromptRelationships:
    """Tests for collection-prompt relationship behaviors."""

    def test_get_prompts_by_collection(self):
        storage = Storage()

        col = Collection(name="Test")
        storage.create_collection(col)

        p1 = Prompt(title="A", content="A", collection_id=col.id)
        p2 = Prompt(title="B", content="B")

        storage.create_prompt(p1)
        storage.create_prompt(p2)

        results = storage.get_prompts_by_collection(col.id)

        assert len(results) == 1
        assert results[0].collection_id == col.id

    def test_delete_collection_with_prompts(self):
        storage = Storage()

        col = Collection(name="Test")
        storage.create_collection(col)

        prompt = Prompt(title="Linked", content="Content", collection_id=col.id)
        storage.create_prompt(prompt)

        result = storage.delete_collection_with_prompts(col.id)

        assert result is True
        assert storage.get_collection(col.id) is None
        assert storage.get_prompt(prompt.id) is None


class TestStorageUtility:
    """Tests for storage utility methods."""

    def test_clear_storage(self):
        storage = Storage()

        col = Collection(name="Test")
        storage.create_collection(col)

        prompt = Prompt(title="Test", content="Content")
        storage.create_prompt(prompt)

        storage.clear()

        assert storage.get_all_prompts() == []
        assert storage.get_all_collections() == []