
import os
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import AzureOpenAIEmbeddings

load_dotenv()

# Create documents covering different topics
docs = [
    # Technology/AI
    Document(page_content="Machine learning models can recognize patterns in data"),
    Document(page_content="Python is a popular programming language for AI"),
    Document(page_content="Neural networks are inspired by the human brain"),
    Document(page_content="Deep learning has revolutionized computer vision"),
    
    # Cooking/Food
    Document(page_content="The recipe calls for flour, eggs, and butter"),
    Document(page_content="Baking a cake requires precise measurements"),
    Document(page_content="Fresh vegetables make healthy salads"),
    
    # Nature/Weather
    Document(page_content="The sunset painted the sky in shades of orange"),
    Document(page_content="Mountains covered in snow look majestic"),
    Document(page_content="The ocean waves crashed against the shore"),
    
    # Sports
    Document(page_content="Football is the most popular sport worldwide"),
    Document(page_content="Running a marathon requires months of training"),
    
    # Music
    Document(page_content="Classical music can help with concentration"),
    Document(page_content="Learning to play guitar takes practice and patience"),
]


def main():
    print(" Similarity Explorer\n")
    print("=" * 80 + "\n")

    # Step 1: Setup embeddings
    embeddings = AzureOpenAIEmbeddings(
        azure_endpoint=os.getenv("AI_ENDPOINT", ""),
        api_key=os.getenv("AI_API_KEY"),
        model=os.getenv("AI_EMBEDDING_MODEL", "text-embedding-3-small"),
        api_version="2024-02-01",
    )

    # Build the vector store from documents
    print(" Building vector store from documents...\n")
    vector_store = InMemoryVectorStore.from_documents(docs, embeddings)

    # Test with different queries
    queries = [
        "How does AI learn?",
        "What ingredients do I need for baking?",
        "Beautiful evening colors"
    ]

    print("=" * 80)
    print("\n SEARCHING WITH DIFFERENT QUERIES\n")
    print("=" * 80 + "\n")

    for query in queries:
        print(f"Query: \"{query}\"")
        print("-" * 60)
        
        # Use similarity_search_with_score to get similarity scores
        results = vector_store.similarity_search_with_score(query, k=3)
        
        for rank, (doc, score) in enumerate(results, 1):
            print(f"   {rank}. Score: {score:.4f} - {doc.page_content}")
        
        print()

    # Demonstrate semantic similarity with different phrasings
    print("=" * 80)
    print("\ SEMANTIC SIMILARITY DEMO")
    print("   (Same meaning, different words)\n")
    print("=" * 80 + "\n")

    semantic_queries = [
        ("How do computers learn from data?", "AI/ML topic"),
        ("Artificial intelligence pattern recognition", "AI/ML topic"),
        ("Making desserts at home", "Cooking topic"),
        ("Ingredients for pastries", "Cooking topic"),
    ]

    for query, expected_topic in semantic_queries:
        print(f"Query: \"{query}\" (Expected: {expected_topic})")
        print("-" * 60)
        
        results = vector_store.similarity_search_with_score(query, k=2)
        
        for rank, (doc, score) in enumerate(results, 1):
            print(f"   {rank}. Score: {score:.4f} - {doc.page_content}")
        
        print()



if __name__ == "__main__":
    main()
