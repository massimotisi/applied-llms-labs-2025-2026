"""
Messages vs Templates - Understanding the Two Paradigms
Run: python 03-prompts-messages-outputs/code/01_messages_vs_templates.py

 Try asking GitHub Copilot Chat (https://github.com/features/copilot):
- "When should I use messages vs templates in LangChain?"
- "How do agents use messages differently from RAG systems?"
"""

import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()


def main():
    print(" Messages vs Templates: Two Approaches\n")
    print("=" * 80)

    model = ChatOpenAI(
        model=os.getenv("AI_MODEL"),
        base_url=os.getenv("AI_ENDPOINT"),
        api_key=os.getenv("AI_API_KEY"),
    )

    # ==========================================
    # APPROACH 1: Messages
    # ==========================================
    print("\n APPROACH 1: Message Arrays\n")

    messages = [
        SystemMessage(content="You are a helpful translator."),
        HumanMessage(content="Translate 'Hello, world!' to French"),
    ]

    print(" Message structure:")
    for i, msg in enumerate(messages):
        print(f'   {i + 1}. {msg.type}: "{msg.content}"')

    message_response = model.invoke(messages)
    print(f"\n Response: {message_response.content}\n")

    print(" Key points about messages:")
    print("   • Direct message construction - no template needed")
    print("   • Used by create_agent() in LangChain")
    print("   • Great for dynamic, conversational flows")
    print("   • Messages can include tool calls and results")
    print("   • Ideal for agents with middleware")

    # ==========================================
    # APPROACH 2: Templates (classic approach)
    # ==========================================
    print("\n" + "=" * 80)
    print("\n APPROACH 2: Templates\n")

    template = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful translator."),
            ("human", "Translate '{text}' to {language}"),
        ]
    )

    print(" Template structure:")
    print("   • System message: Fixed role definition")
    print("   • Human message: Variables {text} and {language}")
    print("   • Reusable across multiple invocations\n")

    template_chain = template | model
    template_response = template_chain.invoke(
        {
            "text": "Hello, world!",
            "language": "French",
        }
    )

    print(f" Response: {template_response.content}\n")

    print(" Key points about templates:")
    print("   • Reusable with variables")
    print("   • Great for consistent prompt structure")
    print("   • Pipes directly to models with | operator")
    print("   • Ideal for structured, repeatable prompts")
    print("   • Easy to version and share across teams")

    # ==========================================
    # WHEN TO USE EACH
    # ==========================================
    print("\n" + "=" * 80)
    print("\n Decision Framework: Which Approach to Use?\n")

    print(" USE MESSAGES when:")
    print("   • Building agents with create_agent()")
    print("   • Working with middleware")
    print("   • Handling multi-step reasoning")
    print("   • Integrating MCP tools")
    print("   • Need full control over message flow")

    print(" USE TEMPLATES when:")
    print("   • Need reusable prompt patterns")
    print("   • Want variable substitution")
    print("   • Building structured workflows with prompt | model")
    print("   • Consistent prompts across application")
    print("   • Sharing prompts across team members")

    print(" Modern LangChain Pattern:")
    print("   • Messages: Dynamic workflows + middleware")
    print("   • Templates: Reusable prompts for consistency")
    print("   • Both are valuable - learn when to use each!")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
