from typing import Dict, Any
from enum import Enum
from tool_strategy import ToolStrategy
from tts_strategy import TTS
from dice_roll import DiceRoller


class ToolType(Enum):
    TTS = 1
    DICE_ROLLER = 2


class Tools:
    def __init__(self):
        self.strategies: Dict[ToolType, ToolStrategy] = {
            ToolType.TTS: TTS(),
            ToolType.DICE_ROLLER: DiceRoller()
        }

    def execute_tool(self, tool_type: ToolType, params: Dict[str, Any]) -> str:
        if tool_type not in self.strategies:
            return f"Error: Tool {tool_type} not found"

        strategy = self.strategies[tool_type]
        return strategy.execute(params)

    def parse_and_execute(self, command: str) -> str:
        # TTS command format: speak:text|voice
        if command.startswith("speak:"):
            parts = command[6:].split("|")
            text = parts[0].strip()
            voice = parts[1].strip() if len(parts) > 1 else "narrator"
            return self.execute_tool(ToolType.TTS, {"text": text, "voice": voice})

        # Dice roll command format: roll:sides
        elif command.startswith("roll:"):
            try:
                sides = int(command[5:].strip())
                return self.execute_tool(ToolType.DICE_ROLLER, {"sides": sides})
            except ValueError:
                return "Error: Invalid dice roll format"

        return f"Error: Unknown command {command}"