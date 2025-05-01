from abc import ABC, abstractmethod
from typing import Dict, Any


class ToolStrategy(ABC):
    """Interface for all tool strategies in the D&D system."""

    @abstractmethod
    def execute(self, params: Dict[str, Any]) -> str:
        """Execute the tool with the given parameters."""
        pass
