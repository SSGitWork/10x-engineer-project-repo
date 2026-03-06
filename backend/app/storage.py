"""In-memory storage for PromptLab

This module provides simple in-memory storage for prompts and collections.
In a production environment, this would be replaced with a database.
"""

from typing import Dict, List, Optional
from app.models import Prompt, Collection


class Storage:
    """In-memory storage for prompts and collections.

    Stores prompts and collections in dictionaries for quick lookup by their IDs.

    Example:
    storage = Storage()
        collection = storage.create_collection(Collection(id="col1", name="My Collection"))
        prompt = storage.create_prompt(Prompt(id="prompt1", name="Greeting", content="Hello", collection_id="col1"))
    """

    def __init__(self):
        """Initialize the in-memory dictionaries for prompts and collections."""
        self._prompts: Dict[str, Prompt] = {}
        self._collections: Dict[str, Collection] = {}

    # ============== Prompt Operations ==============

    def create_prompt(self, prompt: Prompt) -> Prompt:
        """Add a new prompt to the storage.

        Args:
            prompt (Prompt): The Prompt object to store.

        Returns:
            Prompt: The prompt that was added.

        Example:
            storage = Storage()
            prompt = storage.create_prompt(Prompt(id="p1", name="Hi", content="Hello", collection_id="col1"))
        """
        self._prompts[prompt.id] = prompt
        return prompt

    def get_prompt(self, prompt_id: str) -> Optional[Prompt]:
        """Retrieve a prompt by its ID.

        Args:
            prompt_id (str): The ID of the prompt.

        Returns:
            Optional[Prompt]: The prompt if found, otherwise None.

        Example:
            storage = Storage()
            prompt = storage.get_prompt("prompt1")
        """
        return self._prompts.get(prompt_id)

    def get_all_prompts(self) -> List[Prompt]:
        """Get all stored prompts.

        Returns:
            List[Prompt]: A list of all prompts.

        Example:
            storage = Storage()
            all_prompts = storage.get_all_prompts()
        """
        return list(self._prompts.values())

    def update_prompt(self, prompt_id: str, prompt: Prompt) -> Optional[Prompt]:
        """Update an existing prompt.

        Args:
            prompt_id (str): The ID of the prompt to update.
            prompt (Prompt): The new Prompt data.

        Returns:
            Optional[Prompt]: The updated prompt if found, otherwise None.

        Example:
            storage = Storage()
            updated_prompt = storage.update_prompt("prompt1", Prompt(id="prompt1", name="Hi", content="Hello again", collection_id="col1"))
        """
        if prompt_id not in self._prompts:
            return None
        self._prompts[prompt_id] = prompt
        return prompt

    def delete_prompt(self, prompt_id: str) -> bool:
        """Delete a prompt by its ID.

        Args:
            prompt_id (str): The ID of the prompt to delete.

        Returns:
            bool: True if the prompt was deleted, False if it was not found.

        Example:
            storage = Storage()
            success = storage.delete_prompt("prompt1")
        """
        if prompt_id in self._prompts:
            del self._prompts[prompt_id]
            return True
        return False

    # ============== Collection Operations ==============

    def create_collection(self, collection: Collection) -> Collection:
        """Add a new collection to the storage.

        Args:
            collection (Collection): The Collection object to store.

        Returns:
            Collection: The collection that was added.

        Example:
            storage = Storage()
            collection = storage.create_collection(Collection(id="col1", name="My Collection"))
        """
        self._collections[collection.id] = collection
        return collection

    def get_collection(self, collection_id: str) -> Optional[Collection]:
        """Retrieve a collection by its ID.

        Args:
            collection_id (str): The ID of the collection.

        Returns:
            Optional[Collection]: The collection if found, otherwise None.

        Example:
            storage = Storage()
            collection = storage.get_collection("col1")
        """
        return self._collections.get(collection_id)

    def get_all_collections(self) -> List[Collection]:
        """Get all stored collections.

        Returns:
            List[Collection]: A list of all collections.

        Example:
            storage = Storage()
            all_collections = storage.get_all_collections()
        """
        return list(self._collections.values())

    def delete_collection(self, collection_id: str) -> bool:
        """Delete a collection by its ID.

        Args:
            collection_id (str): The ID of the collection to delete.

        Returns:
            bool: True if the collection was deleted, False if it was not found.

        Example:
            storage = Storage()
            success = storage.delete_collection("col1")
        """
        if collection_id in self._collections:
            del self._collections[collection_id]
            return True
        return False

    def get_prompts_by_collection(self, collection_id: str) -> List[Prompt]:
        """Get all prompts associated with a specific collection.

        Args:
            collection_id (str): The ID of the collection.

        Returns:
            List[Prompt]: A list of prompts in the specified collection.

        Example:
            storage = Storage()
            prompts = storage.get_prompts_by_collection("col1")
        """
        return [p for p in self._prompts.values() if p.collection_id == collection_id]

    # ============== Utility ==============

    def clear(self):
        """Clear all stored prompts and collections.

        Example:
            storage = Storage()
            storage.clear()
        """
        self._prompts.clear()
        self._collections.clear()


# Global storage instance
storage = Storage()
