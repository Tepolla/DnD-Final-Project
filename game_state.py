class GameState:
    """Manages the conversation context and tool usage history."""

    def __init__(self, max_history=10):
        """Initialize the game state."""
        self.context_history = []
        self.tool_usage = {}
        self.max_history = max_history

    def update_context(self, message, is_user=True):
        """Add a message to the context history."""
        message_type = "User" if is_user else "System"
        self.context_history.append({"type": message_type, "content": message})

        # Trim history if it gets too long
        if len(self.context_history) > self.max_history:
            self.context_history = self.context_history[-self.max_history:]

    def log_tool_usage(self, tool_name, result):
        """Log tool usage for analytics."""
        if tool_name not in self.tool_usage:
            self.tool_usage[tool_name] = []

        self.tool_usage[tool_name].append(result)

    def get_formatted_context(self):
        """Get the conversation history formatted for the LLM."""
        formatted = "D&D Game Assistant\n\n"

        for message in self.context_history:
            prefix = "User: " if message["type"] == "User" else "Assistant: "
            formatted += prefix + message["content"] + "\n\n"

        formatted += "Assistant: "
        return formatted