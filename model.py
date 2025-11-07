import openai
import dotenv
import logging
import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Load environment variables from .env file
try:
    env = dotenv.dotenv_values(".env")
    YA_API_KEY = env["YA_API_KEY"]
    YA_FOLDER_ID = env["YA_FOLDER_ID"]
except FileNotFoundError:
    raise FileNotFoundError("The .env file was not found. Make sure it exists in the project's root directory.")
except KeyError as e:
    raise KeyError(f"Environment variable {str(e)} not found in .env file. Please check its contents.")


class LLMService:
    """
    A service for interacting with Yandex GPT via the OpenAI-compatible API.

    Parameters:
        prompt_file (str): Path to a system prompt file.
    """

    def __init__(self, prompt_file: str):
        """
        Initialize the LLM service.

        Args:
            prompt_file (str): Path to a file containing the system prompt.
        """
        # Load system prompt from file
        with open(prompt_file, encoding="utf-8") as f:
            self.sys_prompt = f.read()

        try:
            # Create an OpenAI client for Yandex Cloud LLM API
            self.client = openai.OpenAI(
                api_key=YA_API_KEY,
                base_url="https://llm.api.cloud.yandex.net/v1",
            )
            # Build the model path using folder ID from .env
            self.model = f"gpt://{YA_FOLDER_ID}/yandexgpt-lite"

        except Exception as e:
            logger.error(
                f"Error initializing the LLM client. Check your account settings and API key scope. {str(e)}"
            )

    def chat(self, message: str, history: list):
        """
        Send a chat message to the Yandex LLM model.

        Args:
            message (str): The user message.
            history (list): Chat history containing previous messages.

        Returns:
            str: The assistant's reply.
        """
        # Use the last few messages to avoid overloading the context
        messages = (
            [{"role": "system", "content": self.sys_prompt}]
            + history[-4:]
            + [{"role": "user", "content": message}]
        )
        logger.debug(f"Messages: {messages}")

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.3,
                max_tokens=256,
            )
            logger.debug(f"Response: {response}")
            return response.choices[0].message.content

        except Exception as e:
            return f"An error occurred: {str(e)}"


class OllamaService:
    """
    A service for interacting with a local Ollama API.
    """

    def __init__(
        self,
        prompt_file: str,
        base_url: str = "http://localhost:11434",
        model: str = "llama3",
    ):
        """
        Args:
            prompt_file (str): Path to a system prompt file.
            base_url (str): Ollama API base URL.
            model (str): Model name to use.
        """
        with open(prompt_file, encoding="utf-8") as f:
            self.sys_prompt = f.read()
        self.base_url = base_url
        self.model = model

    def chat(self, message: str, history: list):
        """
        Sends a message to Ollama and returns the response.

        Args:
            message (str): User message.
            history (list): Chat history (list of dicts with 'role' and 'content').

        Returns:
            str: Ollama response.
        """
        messages = (
            [{"role": "system", "content": self.sys_prompt}]
            + history[-4:]
            + [{"role": "user", "content": message}]
        )
        payload = {"model": self.model, "messages": messages, "stream": False}

        try:
            response = requests.post(
                f"{self.base_url}/api/chat", json=payload, timeout=60
            )
            response.raise_for_status()
            data = response.json()
            return data["message"]["content"]
        except Exception as e:
            logger.error(f"Ollama error: {str(e)}")
            return f"Ollama error: {str(e)}"


# Initialize main LLM instance
llm_1 = LLMService("prompts/prompt_1.txt")

# Global cache (can be used to store chat sessions or histories)
cache = {}


def chat_with_llm(user_message: str, history: list):
    """
    Communicate with the LLM service.

    Args:
        user_message (str): The user's message.
        history (list): Chat history list.

    Returns:
        str: LLM response.
    """
    llm_response = llm_1.chat(user_message, history)
    history.append({"role": "user", "content": user_message})
    history.append({"role": "assistant", "content": llm_response})
    return llm_response
