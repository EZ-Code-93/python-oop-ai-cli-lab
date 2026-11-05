import ollama


class OllamaChatClient:
    """Generic reusable client for interacting with a local chat model service."""

    def __init__(self, model_name="llama3.2"):
        """
        Initialize the client.

        Requirements:
        - Store the model name.
        - Create an empty list for conversation history.
        - Each client instance should have its own history list.
        """
        self.model_name = model_name
        self.history = []

    def send(self, prompt):
        """
        Send a prompt to the AI service and return the assistant response text.

        Requirements:
        - Reject None, empty, or whitespace-only prompts with ValueError.
        - Strip the prompt before saving it.
        - Add a user message to self.history before calling the service.
        - Call ollama.chat(model=self.model_name, messages=self.history).
        - Extract usable assistant response content.
        - Support both dictionary-style and object-style response shapes.
        - Reject missing, non-string, or blank assistant content.
        - Add the assistant response to self.history only after a usable response.
        - Return the assistant response text.
        - If the service call or response extraction fails:
            - remove the failed user message,
            - preserve previous valid history,
            - raise RuntimeError with a clear service-error message.
        """
        # TODO: Validate the prompt.
        # TODO: Create and append the user message.
        # TODO: Call ollama.chat().
        # TODO: Extract assistant content from the response.
        # TODO: Append the assistant message after a successful response.
        # TODO: Return the assistant response text.
        # TODO: Roll back the failed user message and raise RuntimeError if needed.
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty")
        
        user_message = {
            "role": "user",
            "content": prompt.strip()
        }
        self.history.append(user_message)

        try:
            response = ollama.chat(
                model=self.model_name,
                messages=self.history,
                )

            if isinstance(response, dict):
                message_node = response.get("message")
                if not message_node or not isinstance(message_node, dict):
                    raise ValueError("Unusable dict shape")
                content = message_node.get("content")
                role = message_node.get("role", "assistant")
            else:
                message_node = getattr(response, "message", None)
                if not message_node:
                    raise ValueError("Unusable object shape")
                content = getattr(message_node, "content", None)
                role = getattr(message_node, "role", "assistant")

            # Content verification
            if content is None or not isinstance(content, str) or not content.strip():
                raise ValueError("Content is unusable")

            assistant_message = {"role": role, "content": content}
            self.history.append(assistant_message)
            return content

        except Exception as e:
            self.history.pop()  # Remove failed user message from history
            raise RuntimeError("AI service request failed")

    def reset(self):
        """
        Clear the conversation history.

        Requirements:
        - After this method runs, self.history should be an empty list.
        """
        # TODO: Clear conversation history.
        self.history = []

    def message_count(self):
        """
        Return the number of messages currently stored in conversation history.

        Requirements:
        - Return an integer.
        - Count both user messages and assistant messages.
        """
        # TODO: Return the number of stored messages.
        return len(self.history)

    def get_transcript(self):
        """
        Return a safe copy of the conversation history.

        Requirements:
        - Return a list with the same message dictionaries.
        - Do not return the internal self.history list directly.
        - The returned message dictionaries should also be copies.
        """
        # TODO: Return a copy of the transcript.
        return [msg.copy() for msg in self.history]