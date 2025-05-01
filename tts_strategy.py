from typing import Dict, Any
from tool_strategy import ToolStrategy
from tts_service import KokoroTTSService


class TTS(ToolStrategy):
    """TTS tool strategy implementation."""

    def __init__(self):
        """Initialize the TTS service."""
        self.tts_service = KokoroTTSService()

    def execute(self, params: Dict[str, Any]) -> str:
        """Execute the TTS tool with the given parameters."""
        text = params.get("text", "")
        voice = params.get("voice", "narrator")

        # Generate speech and play it automatically
        _, file_path = self.tts_service.generate_and_play(text, voice)
        return file_path