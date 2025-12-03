"""Dataset model for needle-in-the-groupchat."""

import json
from pathlib import Path
from typing import Iterator

from pydantic import BaseModel, Field

from .conversation import Conversation, PreferenceConversation
from .enums import EvaluationMode


class Dataset(BaseModel):
    """A collection of conversations with load/save capabilities."""

    conversations: list[Conversation] = Field(description="List of conversations in the dataset")

    @classmethod
    def from_directory(cls, path: str | Path) -> "Dataset":
        """Load all conversations from a directory.

        Args:
            path: Directory containing .json conversation files

        Returns:
            Dataset containing all loaded conversations
        """
        path = Path(path)
        if not path.is_dir():
            raise ValueError(f"Path is not a directory: {path}")

        conversations = []
        for json_file in sorted(path.glob("*.json")):
            conv = cls._load_conversation(json_file)
            conversations.append(conv)

        return cls(conversations=conversations)

    @classmethod
    def from_files(cls, paths: list[str | Path]) -> "Dataset":
        """Load conversations from multiple files or directories.

        Args:
            paths: List of paths to .json files or directories

        Returns:
            Dataset containing all loaded conversations
        """
        conversations = []
        for path in paths:
            path = Path(path)
            if path.is_file() and path.suffix == ".json":
                conv = cls._load_conversation(path)
                conversations.append(conv)
            elif path.is_dir():
                for json_file in sorted(path.glob("*.json")):
                    conv = cls._load_conversation(json_file)
                    conversations.append(conv)

        return cls(conversations=conversations)

    @classmethod
    def _load_conversation(cls, path: Path) -> Conversation:
        """Load a single conversation from a JSON file."""
        with open(path) as f:
            data = json.load(f)

        eval_mode = data.get("evaluation_mode", "exact-match")
        if eval_mode == "preference":
            return PreferenceConversation(**data)
        return Conversation(**data)

    def save(self, path: str | Path) -> None:
        """Save all conversations to a directory.

        Args:
            path: Directory to save conversations to
        """
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)

        for conv in self.conversations:
            conv_path = path / f"{conv.id}.json"
            with open(conv_path, "w") as f:
                json.dump(conv.model_dump(), f, indent=2)

    def __iter__(self) -> Iterator[Conversation]:
        """Iterate over conversations in the dataset."""
        return iter(self.conversations)

    def __len__(self) -> int:
        """Return the number of conversations in the dataset."""
        return len(self.conversations)

    def __getitem__(self, index: int) -> Conversation:
        """Get a conversation by index."""
        return self.conversations[index]
