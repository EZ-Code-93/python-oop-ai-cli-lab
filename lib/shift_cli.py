from ai_client import OllamaChatClient
from brief_builder import HandoffBriefBuilder


class ShiftBriefCLI:
    """Command-line workflow for generating and revising shift handoff briefs."""

    def __init__(self, ai_client, brief_builder=None):
        """
        Initialize the CLI application.

        Requirements:
        - Store the injected AI client.
        - Use the provided brief builder when one is passed in.
        - Create a HandoffBriefBuilder when one is not passed in.
        - Set self.running to True.
        """
        self.ai_client = ai_client
        self.brief_builder = brief_builder or HandoffBriefBuilder()
        self.running = True

    def display_welcome(self):
        """
        Print a welcome message and command guidance.

        Requirements:
        - Mention that this is a shift handoff brief CLI.
        - Include the available commands.
        """
        # TODO: Print welcome text and command help.
        print("Welcome to the Shift Handoff Brief CLI!")
        print("Available commands:")
        print(self.command_help())

    def command_help(self):
        """
        Return command guidance as a string.

        Required commands:
        - brief <shift notes>
        - revise <feedback>
        - history
        - reset
        - help
        - exit
        - quit
        """
        # TODO: Return a string describing the available commands.
        return (
            "brief <shift notes> - Create a new handoff brief from shift notes.\n"
            "revise <feedback> - Revise the previous handoff brief based on feedback.\n"
            "history - Show the current message count.\n"
            "reset - Clear conversation history.\n"
            "help - Show this command guidance.\n"
            "exit - Quit the application.\n"
            "quit - Quit the application."
        )

    def handle_command(self, raw_input):
        """
        Route a user command.

        Requirements:
        - Return a readable input error for blank input.
        - Commands should be case-insensitive.
        - Extra spaces around commands should not break the app.
        - brief <shift notes> should call the brief builder's create_brief().
        - revise <feedback> should call the brief builder's revise_brief().
        - history should return the current message count.
        - reset should clear conversation history.
        - help should return command guidance.
        - exit and quit should stop the application.
        - Unknown commands should return a readable input error.
        - ValueError should become a readable Input Error.
        - RuntimeError should become a readable Service Error.
        """
        # TODO: Validate raw_input.
        # TODO: Parse the command and payload.
        # TODO: Route supported commands.
        # TODO: Return helpful messages for errors and unknown commands.
        if not raw_input or not raw_input.strip():
            return "Input Error: Command cannot be blank."
        parts = raw_input.strip().split(maxsplit=1)
        command = parts[0].lower()
        payload = parts[1] if len(parts) > 1 else ""

        try:
            if command == "brief":
                if not payload:
                    return "Input Error: Shift notes cannot be blank."
                return self.brief_builder.create_brief(self.ai_client, payload)
                
            elif command == "revise":
                if not payload:
                    return "Input Error: Revision feedback cannot be blank."
                return self.brief_builder.revise_brief(self.ai_client, payload)
                
            elif command == "history":
                return f"Conversation messages count: {self.ai_client.message_count()}"
                
            elif command == "reset":
                self.ai_client.reset()
                return "Conversation history reset."
                
            elif command == "help":
                return self.command_help()
                
            elif command in ["exit", "quit"]:
                self.running = False
                return "Goodbye!"
                
            else:
                return f"Input Error: Unknown command '{command}'. Use 'help' for layout."

        except ValueError as ve:
            return f"Input Error: {ve}"
        except RuntimeError as re:
            return f"Service Error: {re}"
        

    def run(self):
        """
        Run the CLI input loop.

        Requirements:
        - Display the welcome message before the loop starts.
        - Continue while self.running is True.
        - Read user input.
        - Pass user input to handle_command().
        - Print returned messages.
        - Stop cleanly if EOFError occurs.
        """
        # TODO: Display welcome text.
        # TODO: Run the input loop.
        self.display_welcome()
        while self.running:
            try:
                user_input = input("> ")
                message = self.handle_command(user_input)
                print(message)
            except EOFError:
                self.running = False
                print("Goodbye!")
                break


def main():
    client = OllamaChatClient(model_name="llama3.2")
    app = ShiftBriefCLI(client)
    app.run()


if __name__ == "__main__":
    main()