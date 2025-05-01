from tools import Tools, ToolType
from game_state import GameState
from llama_llm import LlamaLLM
import textwrap
import re


class Main:
    def __init__(self, model_path):
        self.llm = LlamaLLM(model_path)
        self.tools = Tools()
        self.state = GameState()
        self.console_width = 70  # For text wrapping

    def process_input(self, user_input: str) -> str:
        # Check if this is a dice roll request
        if re.search(r'roll\s+(for|a|the)?', user_input.lower()):
            return self._handle_dice_roll(user_input)
        else:
            return self._handle_normal_input(user_input)

    def _handle_dice_roll(self, user_input: str) -> str:
        """Handle dice roll requests specially"""
        # Update context with user input
        self.state.update_context(user_input, is_user=True)

        # Determine dice type (default to D20)
        dice_sides = 20
        dice_match = re.search(r'd(\d+)', user_input.lower())
        if dice_match:
            dice_sides = int(dice_match.group(1))

        # Roll the dice
        dice_result = self.tools.execute_tool(ToolType.DICE_ROLLER, {"sides": dice_sides})

        # Format the roll result message
        roll_message = f"You rolled a {dice_result} on a D{dice_sides}."
        print(f"\nD&D System: {roll_message}")

        # Add roll result to context for LLM to see
        roll_context = f"The player rolled a {dice_result} on a D{dice_sides}."
        self.state.update_context(roll_context, is_user=False)

        # Generate LLM response based on roll
        prompt = self.state.get_formatted_context()
        llm_response = self.llm.generate(prompt)

        # Add LLM response to context
        self.state.update_context(llm_response, is_user=False)

        # Speak the entire response with TTS
        self.tools.execute_tool(ToolType.TTS, {"text": llm_response, "voice": "narrator"})

        return f"{roll_message}\n\n{llm_response}"

    def _handle_normal_input(self, user_input: str) -> str:
        """Handle normal (non-dice) input"""
        # Update context with user input
        self.state.update_context(user_input, is_user=True)

        # Generate LLM response
        prompt = self.state.get_formatted_context()
        llm_response = self.llm.generate(prompt)

        # Process and extract tool commands from the response
        processed_response, remaining_text = self._process_tool_commands(llm_response)

        # If there's text left after processing commands, speak it with TTS
        if remaining_text.strip():
            self.tools.execute_tool(ToolType.TTS, {"text": remaining_text, "voice": "narrator"})

        # Add original LLM response to context history
        self.state.update_context(llm_response, is_user=False)

        return processed_response

    def _process_tool_commands(self, text):
        """Process tool commands in the text and return processed text + remainder"""
        response_parts = []
        remaining_text = text

        while "[[" in remaining_text and "]]" in remaining_text:
            start_idx = remaining_text.find("[[")
            end_idx = remaining_text.find("]]", start_idx)

            if start_idx > 0:
                response_parts.append(remaining_text[:start_idx])

            command = remaining_text[start_idx + 2:end_idx]
            print(f"Executing command: {command}")

            # Execute command
            self.tools.parse_and_execute(command)

            # Move past this command
            remaining_text = remaining_text[end_idx + 2:]

        # Return both the processed parts and any remaining text
        return "".join(response_parts) + remaining_text, remaining_text

    def handle_output(self, response: str) -> None:
        print("\nD&D System Response:")
        wrapped = textwrap.fill(response, width=self.console_width)
        print(wrapped)
        print("\n" + "-" * 50)

    def run_interaction(self, user_input: str) -> str:
        response = self.process_input(user_input)
        self.handle_output(response)
        return response

    def run_interactive_session(self):
        print("\n" + "=" * 50)
        print("Welcome to the D&D LLM Assistant!")
        print("Enter your queries or commands.")
        print("To roll dice, type something like 'roll for perception' or 'roll d20'")
        print("Type '<Save>' to exit and save the conversation (any case works).")
        print("=" * 50 + "\n")

        # Prime the LLM with instructions
        self.state.update_context(
            "You are a D&D game assistant who responds to player actions and questions. "
            "When a player rolls dice, incorporate the result into your response naturally. "
            "Describe scenes vividly and in character.",
            is_user=False
        )

        while True:
            user_input = input("\nYou: ")
            if user_input.strip().lower() == "<save>":
                print("\nSaving conversation and exiting...")
                self.save_conversation()
                break
            self.run_interaction(user_input)

    def save_conversation(self, filename="conversation.txt"):
        with open(filename, "w") as f:
            f.write("D&D LLM Conversation\n")
            f.write("=" * 30 + "\n\n")
            for message in self.state.context_history:
                prefix = "User: " if message["type"] == "User" else "System: "
                f.write(prefix + message["content"] + "\n\n")
        print(f"Conversation saved to {filename}")


if __name__ == "__main__":
    model_path = "C:\\Users\\Derek\\OneDrive\\Desktop\\PythonProj\\DnD_Project\\models\\llama3.1-8b-instruct-q4_K_M.gguf"
    system = Main(model_path)
    system.run_interactive_session()
