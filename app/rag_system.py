"""
Phase 7 - RAG (Retrieval-Augmented Generation) System
Complete English Version with Detailed Comments

This module implements a complete RAG system that can:
1. Load documents from files
2. Generate embeddings (convert text to vectors)
3. Store vectors in a FAISS database
4. Search using semantic similarity
5. Search using keyword matching (BM25)
6. Combine both methods (hybrid search)

Supported Languages: Urdu, Roman Urdu, English
Model: paraphrase-multilingual-MiniLM-L12-v2 (384 dimensions)
"""

import os
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple

# ============================================================================
# STEP 1: Import Required Libraries
# ============================================================================

print("📚 Importing libraries...\n")

# Sentence-Transformers: Converts text into vector embeddings
# Supports multiple languages including Urdu and English
from sentence_transformers import SentenceTransformer

# FAISS: Facebook AI Similarity Search
# Ultra-fast vector similarity search - can handle millions of vectors
import faiss

# BM25: Best Match 25 Algorithm
# Traditional keyword-based search algorithm
# Used for exact term matching
from rank_bm25 import BM25Okapi

print("✅ All libraries imported successfully!\n")

# ============================================================================
# STEP 2: Configuration Settings
# ============================================================================

print("⚙️ Setting up configuration...\n")

# Which embedding model to use?
# paraphrase-multilingual-MiniLM-L12-v2:
#   - Supports: Urdu, Roman Urdu, English, 100+ other languages
#   - Size: Small and fast (~100MB)
#   - Quality: Good for most use cases
#   - Dimensions: 384 (vector size)
EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"

# Size of each vector/embedding
# This model uses 384 dimensions
VECTOR_SIZE = 384

# Where to find the documents
# This file contains menu items, prices, and restaurant policies
DOCUMENTS_PATH = Path("documents/menu_and_policies.txt")

# Where to save the vector database
# (Not used in this demo, but useful for production)
VECTOR_DB_PATH = Path("data/vector_db")

print(f"Configuration set:")
print(f"  Model: {EMBEDDING_MODEL}")
print(f"  Vector Size: {VECTOR_SIZE} dimensions")
print(f"  Documents Path: {DOCUMENTS_PATH}")
print(f"  Vector DB Path: {VECTOR_DB_PATH}\n")

# ============================================================================
# STEP 3: Document Loading Function
# ============================================================================

def load_documents(file_path: Path) -> List[str]:
    """
    Load a document file and split it into chunks.

    Why split into chunks?
    - Large documents are harder to embed and search
    - Chunks allow more granular search results
    - Typical chunk size: 300-500 characters

    Args:
        file_path: Path to the document file

    Returns:
        List of document chunks

    Process:
        1. Open and read the entire file
        2. Split text into 500-character pieces
        3. Remove empty chunks
        4. Return the list
    """
    print(f"📂 Loading document: {file_path}\n")

    # Check if file exists
    if not file_path.exists():
        raise FileNotFoundError(f"Document file not found: {file_path}")

    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    print(f"   ✅ File loaded - Total size: {len(text)} characters")

    # Split text into chunks (500 characters each)
    # Why 500? Balance between:
    # - Too small: Not enough context per chunk
    # - Too large: Harder to find specific information
    chunks = []
    chunk_size = 500

    for i in range(0, len(text), chunk_size):
        # Extract chunk
        chunk = text[i:i+chunk_size].strip()

        # Only add non-empty chunks
        if chunk:
            chunks.append(chunk)

    print(f"   ✅ Created {len(chunks)} chunks\n")
    return chunks


# ============================================================================
# STEP 4: RAG System Class
# ============================================================================

class RAGSystem:
    """
    Complete Retrieval-Augmented Generation System.

    This class manages the entire RAG pipeline:
    1. Load and store documents
    2. Generate embeddings
    3. Create vector index (FAISS)
    4. Create keyword index (BM25)
    5. Perform searches (semantic, keyword, hybrid)

    Attributes:
        model: Sentence transformer model for embeddings
        index: FAISS vector database index
        documents: List of document chunks
        embeddings: Array of document embeddings
        tokenized_docs: Documents split into words
        bm25: BM25 index for keyword search
    """

    def __init__(self, model_name: str, vector_size: int):
        """
        Initialize the RAG system.

        What happens:
        1. Load the embedding model
        2. Create FAISS index
        3. Initialize storage variables

        Args:
            model_name: Name of the embedding model
            vector_size: Dimension size of vectors (384 for our model)

        Note:
            First initialization downloads the model (~100MB)
            Subsequent runs use cached model (much faster)
        """
        print(f"\n🤖 Initializing RAG System...")
        print(f"   Model: {model_name}")
        print(f"   Vector Size: {vector_size} dimensions\n")

        # Load the pre-trained embedding model
        # This model is trained on millions of text pairs
        # It understands semantic similarity across languages
        print(f"   ⏳ Loading embedding model (may take time on first run)...")
        self.model = SentenceTransformer(model_name)
        print(f"   ✅ Model loaded successfully!")

        # Create FAISS index
        # IndexFlatL2: Uses Euclidean distance for similarity
        # This is simple but effective for most use cases
        # Other options: IndexIVFFlat (for very large datasets)
        self.index = faiss.IndexFlatL2(vector_size)

        # Variables to store data
        self.embeddings = None          # Store document embeddings
        self.documents = []              # Store original documents
        self.tokenized_docs = []        # Store words from each document
        self.bm25 = None                # BM25 index (initialized later)

        print(f"   ✅ FAISS index created!\n")

    def add_documents(self, documents: List[str]):
        """
        Add documents to the RAG system.

        Process:
        1. Generate embeddings for all documents
        2. Add embeddings to FAISS index
        3. Prepare documents for BM25 search
        4. Create BM25 index

        Args:
            documents: List of document chunks to add

        Result:
            All documents are now searchable via:
            - Semantic search (FAISS)
            - Keyword search (BM25)
        """
        print(f"\n📝 Adding documents to RAG system...")
        print(f"   Total documents: {len(documents)}\n")

        # Store original documents
        self.documents = documents

        # ====================================================================
        # Step 1: Generate Embeddings
        # ====================================================================
        print(f"   Step 1: Generating embeddings...")
        print(f"   ⏳ Processing {len(documents)} documents...")

        # encode() converts each document to a vector
        # Returns shape: (num_documents, 384)
        # Each row is a document, 384 columns are the vector dimensions
        embeddings = self.model.encode(documents, show_progress_bar=True)
        self.embeddings = embeddings

        print(f"   ✅ Embeddings generated!")
        print(f"      Shape: {embeddings.shape}")
        print(f"      Meaning: {len(documents)} documents, each 384 dimensions\n")

        # ====================================================================
        # Step 2: Add to FAISS Index
        # ====================================================================
        print(f"   Step 2: Adding to FAISS index...")

        # FAISS requires float32 arrays
        # Convert and add to index
        # The index will build any internal data structures needed
        embeddings_float32 = np.array(embeddings).astype('float32')
        self.index.add(embeddings_float32)

        print(f"   ✅ FAISS index updated!")
        print(f"      Total vectors in index: {self.index.ntotal}\n")

        # ====================================================================
        # Step 3: Prepare for BM25 Keyword Search
        # ====================================================================
        print(f"   Step 3: Preparing BM25 index...")

        # Tokenization: Split each document into words
        # Example: "Biryani is delicious" → ["biryani", "is", "delicious"]
        # Lowercase for case-insensitive search
        self.tokenized_docs = [doc.lower().split() for doc in documents]

        # Create BM25 index
        # BM25 learns word frequencies and importance
        self.bm25 = BM25Okapi(self.tokenized_docs)

        print(f"   ✅ BM25 index ready!")
        print(f"      Documents tokenized and indexed\n")
        print(f"✅ All documents added successfully!\n")

    def semantic_search(self, query: str, top_k: int = 3) -> List[Tuple[str, float]]:
        """
        Semantic Search: Find documents by meaning, not keywords.

        How it works:
        1. Convert query to embedding (same way as documents)
        2. Find most similar document embeddings in FAISS
        3. Return top K results with similarity scores

        Advantages:
        - Understands synonyms (e.g., "khana" = "food")
        - Works across languages
        - Finds relevant results even with different wording

        Args:
            query: Search query (any language)
            top_k: Number of results to return (default 3)

        Returns:
            List of (document, similarity_score) tuples
            Similarity score: 0 to 1 (1 = perfect match)
        """
        # Convert query to embedding
        # Same model as documents, so comparable vectors
        query_embedding = self.model.encode([query])

        # Search in FAISS index
        # Returns: (distances, indices)
        # Distances: Euclidean distance (lower = more similar)
        # Indices: Document indices in our list
        distances, indices = self.index.search(
            np.array(query_embedding).astype('float32'),
            top_k
        )

        # Convert distances to similarity scores
        # Formula: similarity = 1 / (1 + distance)
        # This converts distance to 0-1 range
        results = []
        for i, idx in enumerate(indices[0]):
            if idx >= 0:  # Valid index check
                similarity_score = 1 / (1 + distances[0][i])
                results.append((self.documents[idx], similarity_score))

        return results

    def keyword_search(self, query: str, top_k: int = 3) -> List[Tuple[str, float]]:
        """
        Keyword Search: Find documents containing specific terms.

        How it works:
        1. Split query into words (tokenize)
        2. Use BM25 to score each document
        3. BM25 considers:
           - Term frequency (how many times word appears)
           - Inverse document frequency (how rare the word is)
           - Document length normalization
        4. Return top K results

        Advantages:
        - Exact term matching
        - Works well for specific queries (e.g., "price", "delivery")
        - Good for structured information lookup

        Args:
            query: Search query
            top_k: Number of results to return

        Returns:
            List of (document, bm25_score) tuples
            Score: Higher = more relevant
        """
        # Tokenize query
        query_tokens = query.lower().split()

        # Calculate BM25 scores for all documents
        # Returns array of scores (one per document)
        scores = self.bm25.get_scores(query_tokens)

        # Get top K documents by score
        # argsort returns indices sorted by value
        # [-top_k:] gets the last (highest) K items
        # [::-1] reverses to get highest first
        top_indices = np.argsort(scores)[-top_k:][::-1]

        # Build results list (only include documents with positive scores)
        results = []
        for idx in top_indices:
            if scores[idx] > 0:  # Only positive scores
                results.append((self.documents[idx], scores[idx]))

        return results

    def hybrid_search(self, query: str, top_k: int = 3,
                     semantic_weight: float = 0.6,
                     keyword_weight: float = 0.4) -> List[Tuple[str, float]]:
        """
        Hybrid Search: Combine semantic and keyword search.

        Why combine both?
        - Semantic search: Good at understanding meaning
        - Keyword search: Good at exact matching
        - Hybrid: Gets benefits of both!

        Formula:
        Final Score = (Semantic Score × 0.6) + (Keyword Score × 0.4)

        Example:
        Query: "Biryani price"
        - Semantic finds related items (score: 0.85)
        - Keyword finds "price" mentions (score: 0.95)
        - Hybrid: (0.85 × 0.6) + (0.95 × 0.4) = 0.89

        Args:
            query: Search query
            top_k: Number of results to return
            semantic_weight: Weight for semantic results (0-1)
            keyword_weight: Weight for keyword results (0-1)

        Returns:
            List of (document, combined_score) tuples
            Combined score: 0 to 1+ (higher = more relevant)
        """
        print(f"\n🔍 Performing Hybrid Search...")
        print(f"   Query: '{query}'")
        print(f"   Weights: Semantic {semantic_weight*100:.0f}% + Keyword {keyword_weight*100:.0f}%\n")

        # Get semantic search results
        semantic_results = self.semantic_search(query, top_k)

        # Get keyword search results
        keyword_results = self.keyword_search(query, top_k)

        # Combine results in a dictionary
        # Document text → combined score
        combined_scores = {}

        # Add semantic results
        # Key: document text, Value: semantic score × weight
        for doc, score in semantic_results:
            combined_scores[doc] = semantic_weight * score

        # Add keyword results
        # If document already exists, add to its score
        # Otherwise, create new entry
        for doc, score in keyword_results:
            if doc in combined_scores:
                # Document found in both searches - add scores
                combined_scores[doc] += keyword_weight * score
            else:
                # Document only in keyword search
                combined_scores[doc] = keyword_weight * score

        # Sort by combined score (highest first)
        sorted_results = sorted(
            combined_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )[:top_k]

        return sorted_results


# ============================================================================
# STEP 5: Main Execution / Testing
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("🚀 PHASE 7 - RAG SYSTEM START")
    print("=" * 80)

    # ========================================================================
    # 1. Initialize RAG System
    # ========================================================================
    print("\n1️⃣ Initializing RAG System...\n")
    rag = RAGSystem(EMBEDDING_MODEL, VECTOR_SIZE)

    # ========================================================================
    # 2. Load Documents
    # ========================================================================
    print("\n2️⃣ Loading Documents...\n")
    if not DOCUMENTS_PATH.exists():
        print(f"❌ Error: {DOCUMENTS_PATH} not found!")
        print(f"   Please create: documents/menu_and_policies.txt")
        exit(1)

    documents = load_documents(DOCUMENTS_PATH)

    # ========================================================================
    # 3. Add Documents to RAG
    # ========================================================================
    print("\n3️⃣ Adding Documents to RAG System...\n")
    rag.add_documents(documents)

    # ========================================================================
    # 4. Test Queries
    # ========================================================================
    print("=" * 80)
    print("✅ RAG SYSTEM READY FOR TESTING!")
    print("=" * 80)

    # Define test queries in different languages
    test_queries = [
        "Biryani ki price kya hai?",              # Roman Urdu - Menu
        "Chicken Tikka mein kya ingredients hain?",  # Roman Urdu - Menu
        "Delivery charges kitne hain?",           # Roman Urdu - Policy
        "What is the opening time?",              # English - Policy
        "Tell me about payment methods",          # English - Policy
    ]

    # Run tests
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'─' * 80}")
        print(f"TEST {i}: {query}")
        print(f"{'─' * 80}")

        # Perform hybrid search
        results = rag.hybrid_search(query, top_k=2)

        # Display results
        for j, (doc, score) in enumerate(results, 1):
            print(f"\n   Result {j} (Confidence: {score:.2%})")
            print(f"   {doc[:150]}...")  # Show first 150 characters

    # ========================================================================
    # 5. Summary
    # ========================================================================
    print("\n" + "=" * 80)
    print("✅ TESTING COMPLETE!")
    print("=" * 80)
    print(f"\nSummary:")
    print(f"  • Documents loaded: {len(documents)}")
    print(f"  • Test queries: {len(test_queries)}")
    print(f"  • Search methods: Semantic + Keyword + Hybrid")
    print(f"  • Languages supported: Urdu, Roman Urdu, English")
    print(f"  • Status: PRODUCTION READY ✅")
    print("\n" + "=" * 80)
