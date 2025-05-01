import random
from typing import Dict, Any
from tool_strategy import ToolStrategy


def roll_dice(sides):
    MIN_SIDES = 2
    MAX_SIDES = 100  # DnD dice rarely go above d100

    if sides < MIN_SIDES:
        return "<[too low]>"
    elif sides > MAX_SIDES:
        return "<[too high]>"
    else:
        return random.randint(1, sides)


class DiceRoller(ToolStrategy):
    """Dice roller tool strategy implementation."""

    def execute(self, params: Dict[str, Any]) -> str:
        """Execute the dice roller with the given parameters."""
        sides = params.get("sides", 20)
        result = roll_dice(sides)
        return str(result)
