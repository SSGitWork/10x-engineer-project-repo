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
        """Create and store a new prompt.

        Adds the provided Prompt object to the in-memory prompt dictionary,
        keyed by its unique identifier.
        Args:
            prompt (Prompt): The Prompt instance to store, including its id,
                name, content, and associated collection_id.

        Returns:
            Prompt: The stored Prompt object.

        Example:
            storage = Storage()
            prompt = Prompt(
                id="p1",
                name="Greeting",
                content="Hello, world",
                collection_id="col1",
            )
            created_prompt = storage.create_prompt(prompt)
        """
        self._prompts[prompt.id] = prompt
        return prompt

    def get_prompt(self, prompt_id: str) -> Optional[Prompt]:
        """Retrieve a prompt by its unique identifier.

        Looks up the prompt in the in-memory storage dictionary.

        Args:
            prompt_id (str): The unique identifier of the prompt to retrieve.

        Returns:
            Optional[Prompt]: The matching Prompt if it exists, otherwise None.
        Example:
            storage = Storage()
            prompt = storage.get_prompt("p1")
            if prompt:
                print(prompt.name)
        """
        return self._prompts.get(prompt_id)

    def get_all_prompts(self) -> List[Prompt]:
        """Retrieve all stored prompts.

        Returns all Prompt objects currently stored in memory.

        Args:
            None
        Returns:
            List[Prompt]: A list containing all stored Prompt objects.

        Example:
            storage = Storage()
            prompts = storage.get_all_prompts()
            for prompt in prompts:
                print(prompt.name)
        """
        return list(self._prompts.values())

    def update_prompt(self, prompt_id: str, prompt: Prompt) -> Optional[Prompt]:
        """Update an existing prompt in storage.

        Replaces the stored prompt with the provided Prompt object if the
        prompt_id exists in the storage.

        Args:
            prompt_id (str): The identifier of the prompt to update.
            prompt (Prompt): The new Prompt object that will replace the
                existing stored prompt.

        Returns:
            Optional[Prompt]: The updated Prompt if the prompt existed,
                otherwise None.

        Example:
            storage = Storage()
            updated = storage.update_prompt(
                "p1",
                Prompt(
                    id="p1",
                    name="Greeting Updated",
                    content="Hello again",
                    collection_id="col1",
                ),
            )
        """
        if prompt_id not in self._prompts:
            return None
        self._prompts[prompt_id] = prompt
        return prompt

    def delete_prompt(self, prompt_id: str) -> bool:
        """Delete a prompt from storage by its identifier.

        Removes the prompt from the in-memory dictionary if it exists.

        Args:
            prompt_id (str): The unique identifier of the prompt to delete.

        Returns:
            bool: True if the prompt was successfully deleted, False if
                no prompt with the given ID exists.

        Example:
            storage = Storage()
            success = storage.delete_prompt("p1")
            if success:
                print("Prompt deleted")
        """
        if prompt_id in self._prompts:
            del self._prompts[prompt_id]
            return True
        return False

    # ============== Collection Operations ==============

    def create_collection(self, collection: Collection) -> Collection:
        """Create and store a new collection.

        Adds the provided Collection object to the in-memory collection
        dictionary, keyed by its unique identifier.
        Args:
            collection (Collection): The Collection instance to store, including
                its unique id and name.

        Returns:
            Collection: The stored Collection object.

        Example:
            storage = Storage()
            collection = Collection(id="col1", name="My Collection")
            created_collection = storage.create_collection(collection)
            print(created_collection.name)
        """
        self._collections[collection.id] = collection
        return collection

    def get_collection(self, collection_id: str) -> Optional[Collection]:
        """Retrieve a collection by its unique identifier.

        Looks up the collection in the in-memory storage dictionary.

        Args:
            collection_id (str): The unique identifier of the collection
                to retrieve.

        Returns:
            Optional[Collection]: The matching Collection if it exists,
                otherwise None.

        Example:
            storage = Storage()
            collection = storage.get_collection("col1")
            if collection:
                print(collection.name)
        """
        return self._collections.get(collection_id)

    def collection_exists(self, collection_id: str) -> bool:
        """Check whether a collection exists in storage.

        Verifies if the provided collection identifier is present in the
        in-memory collection dictionary.

        Args:
            collection_id (str): The unique identifier of the collection.

        Returns:
            bool: True if the collection exists, otherwise False.
        Example:
            storage = Storage()
            exists = storage.collection_exists("col1")
            print(exists)
        """
        return collection_id in self._collections

    def get_all_collections(self) -> List[Collection]:
        """Retrieve all stored collections.

        Returns all Collection objects currently stored in memory.
        Args:
            None
        Returns:
            List[Collection]: A list containing all stored Collection objects.
        Example:
            storage = Storage()
            collections = storage.get_all_collections()
            for collection in collections:
                print(collection.name)
        """
        return list(self._collections.values())
    def delete_collection(self, collection_id: str) -> bool:
        """Delete a collection from storage by its identifier.

        Removes the collection from the in-memory dictionary if it exists.

        Args:
            collection_id (str): The unique identifier of the collection
                to delete.

        Returns:
            bool: True if the collection was successfully deleted,
                False if no collection with the given ID exists.

        Example:
            storage = Storage()
            success = storage.delete_collection("col1")
            if success:
                print("Collection deleted")
        """
        if collection_id in self._collections:
            del self._collections[collection_id]
            return True
        return False

    def get_prompts_by_collection(self, collection_id: str) -> List[Prompt]:
        """Retrieve all prompts associated with a specific collection.

        Filters stored prompts and returns those whose collection_id matches
        the provided collection identifier.

        Args:
            collection_id (str): The unique identifier of the collection.

        Returns:
            List[Prompt]: A list of Prompt objects that belong to the
                specified collection.

        Example:
            storage = Storage()
            prompts = storage.get_prompts_by_collection("col1")
            for prompt in prompts:
                print(prompt.name)
        """
        return [p for p in self._prompts.values() if p.collection_id == collection_id]

    def delete_collection_with_prompts(self, collection_id: str) -> bool:
        """Delete a collection and all prompts associated with it.

        Removes the specified collection and deletes any prompts whose
        collection_id references the collection.

        Args:
            collection_id (str): The unique identifier of the collection
                to delete.

        Returns:
            bool: True if the collection existed and was deleted,
                otherwise False.

        Example:
            storage = Storage()
            success = storage.delete_collection_with_prompts("col1")
            if success:
                print("Collection and associated prompts deleted")
        """
        if collection_id not in self._collections:
            return False

        prompts_to_delete = [
            p.id for p in self._prompts.values() if p.collection_id == collection_id
        ]

        for prompt_id in prompts_to_delete:
            del self._prompts[prompt_id]

        del self._collections[collection_id]
        return True

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
