"""
Product Data Extractor with Structured Outputs
Run: python 03-prompts-messages-outputs/solution/product_extractor.py
"""

import os
from typing import Literal

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()


# Define product schema with validation
class Product(BaseModel):
    """Extracted product information."""

    name: str = Field(description="Product name")
    price: float = Field(description="Price in USD")
    category: Literal["Electronics", "Clothing", "Food", "Books", "Home"] = Field(
        description="Product category"
    )
    in_stock: bool = Field(description="Whether the product is currently available")
    rating: float = Field(ge=1, le=5, description="Customer rating from 1-5 stars")
    features: list[str] = Field(
        description="List of key product features or highlights"
    )


def main():
    print(" Product Data Extractor with Structured Outputs\n")

    model = ChatOpenAI(
        model=os.getenv("AI_MODEL"),
        base_url=os.getenv("AI_ENDPOINT"),
        api_key=os.getenv("AI_API_KEY"),
    )

    # Create structured model
    structured_model = model.with_structured_output(Product)

    # Create a prompt template
    template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """Extract product information from the description.
If a field is not explicitly mentioned, make a reasonable inference.
Ensure the category is one of: Electronics, Clothing, Food, Books, or Home.""",
            ),
            ("human", "{description}"),
        ]
    )

    # Combine template with structured output
    chain = template | structured_model

    # Test data
    products = [
        {
            "name": "Tech Product",
            "description": """MacBook Pro 16-inch with M3 chip, $2,499. Currently in stock.
                Users rate it 4.8/5. Features: Liquid Retina display, 18-hour battery, 1TB SSD""",
        },
        {
            "name": "Clothing Item",
            "description": """Cozy wool sweater, blue color, medium size. $89, available now!
                Customers love it - 4.5 stars. Hand-washable, made in Ireland""",
        },
        {
            "name": "Book",
            "description": """The Great Gatsby by F. Scott Fitzgerald. Classic novel, paperback edition for $12.99.
                In stock. Rated 4.9 stars. 180 pages, published 1925""",
        },
        {
            "name": "Home Item",
            "description": """Modern LED desk lamp with adjustable brightness. $45.99.
                Available for immediate shipping. 4.6 star rating. USB charging, touch controls, energy efficient""",
        },
        {
            "name": "Food Product",
            "description": """Organic dark chocolate bar, 85% cacao. $5.99 each.
                In stock! Rated 4.7 stars by health-conscious buyers. Fair trade, vegan, no added sugar""",
        },
    ]

    print(" Extracting product data from descriptions:\n")
    print("=" * 80)

    for i, product in enumerate(products, 1):
        print(f"\n{i} {product['name']}:\n")

        try:
            result = chain.invoke({"description": product["description"]})

            print(" Extracted Data:")
            print(result.model_dump_json(indent=2))

            # Type-safe access to fields
            print("\n Formatted Output:")
            print(f"    {result.name}")
            print(f"    ${result.price:.2f}")
            print(f"   Category: {result.category}")
            print(f"    {' In Stock' if result.in_stock else ' Out of Stock'}")
            print(f"    Rating: {result.rating}/5")
            print("    Features:")
            for feature in result.features:
                print(f"      • {feature}")

            print("\n" + "=" * 80)
        except Exception as error:
            print(f" Error extracting data: {error}")
            print("=" * 80)


if __name__ == "__main__":
    main()
