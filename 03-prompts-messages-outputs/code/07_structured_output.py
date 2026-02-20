"""
Structured Output Example
Run: python 03-prompts-messages-outputs/code/07_structured_output.py

 Try asking GitHub Copilot Chat (https://github.com/features/copilot):
- "How does with_structured_output() ensure the response matches the schema?"
- "Can I make some Pydantic model fields optional instead of required?"
"""

import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, EmailStr, Field

# Load environment variables
load_dotenv()


# Define the structure using Pydantic model
class Person(BaseModel):
    """Information about a person."""

    name: str = Field(description="The person's full name")
    age: int = Field(description="The person's age in years")
    email: str = Field(description="The person's email address")
    occupation: str = Field(description="The person's job or profession")


def main():
    print(" Structured Output Example\n")

    model = ChatOpenAI(
        model=os.getenv("AI_MODEL"),
        base_url=os.getenv("AI_ENDPOINT"),
        api_key=os.getenv("AI_API_KEY"),
    )

    # Create a model that returns structured output
    structured_model = model.with_structured_output(Person)

    print(" Testing with different inputs:\n")
    print("=" * 80)

    # Test 1: Complete information
    print("\n1  Complete Information:\n")
    result1 = structured_model.invoke(
        "My name is Alice Johnson, I'm 28 years old, work as a software engineer, "
        "and you can reach me at alice.j@email.com"
    )

    print(" Structured Output (typed!):")
    print(result1.model_dump_json(indent=2))
    print("\n Type-safe field access:")
    print(f"   Name: {result1.name}")
    print(f"   Age: {result1.age} years old")
    print(f"   Email: {result1.email}")
    print(f"   Occupation: {result1.occupation}")

    # Test 2: Casual conversation
    print("\n" + "=" * 80)
    print("\n2  From Casual Conversation:\n")
    result2 = structured_model.invoke(
        "Hey! I'm Bob, a 35-year-old data scientist. You can email me at bob.smith@company.com"
    )

    print(" Extracted Data:")
    print(result2.model_dump_json(indent=2))

    # Test 3: Resume-like format
    print("\n" + "=" * 80)
    print("\n3  From Resume Text:\n")
    result3 = structured_model.invoke(
        "Sarah Martinez | Marketing Director | Age: 42 | Contact: sarah.m@marketing.co"
    )

    print(" Parsed Resume:")
    print(result3.model_dump_json(indent=2))

    print("\n" + "=" * 80)
    print("\n Benefits of Structured Outputs:")
    print("   -  Type-safe data access (Python knows the types!)")
    print("   -  No manual parsing needed")
    print("   -  Validation built-in (age is int, email is valid)")
    print("   -  Consistent format regardless of input style")
    print("   -  Easy to integrate with databases, APIs, and UI")


if __name__ == "__main__":
    main()
