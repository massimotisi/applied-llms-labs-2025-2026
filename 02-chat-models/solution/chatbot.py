"""
Challenge 1 Solution: Interactive Chatbot
Run: python 02-chat-models/solution/chatbot.py
"""

import os

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()

model = ChatOpenAI(
    model=os.environ.get("AI_MODEL", "gpt-5-mini"),
    base_url=os.getenv("AI_ENDPOINT"),
    api_key=os.getenv("AI_API_KEY"),
)

messages = [
    SystemMessage(
        content="You are a friendly and helpful AI assistant. Be conversational and warm in your responses."
    ),
]


def chat():
    """Interactive chat loop with conversation history."""
    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n\n Goodbye! We had {len(messages)} messages in our conversation.")
            break

        if user_input.lower() in ("quit", "exit"):
            print(f"\n Goodbye! We had {len(messages)} messages in our conversation.")
            break

        if not user_input:
            continue

        messages.append(HumanMessage(content=user_input))

        try:
            response = model.invoke(messages)
            print(f"\n Chatbot: {response.content}")

            messages.append(AIMessage(content=str(response.content)))
            print(f" Conversation length: {len(messages)} messages")

            # Exit in CI mode after one interaction
            if os.environ.get("CI") == "true":
                break

        except Exception as error:
            print(f"\n Error: {error}")


def main():
    print(" Chatbot: Hello! I'm your helpful assistant. Ask me anything!")
    print('(Type "quit" to exit)\n')

    chat()


if __name__ == "__main__":
    main()
