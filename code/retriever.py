import os
import re
from collections import defaultdict

CORPUS_DIR = "corpus"

COMPANY_MAP = {
    "hackerrank": "hackerrank",
    "claude": "claude",
    "visa": "visa",
    "none": None
}

def load_corpus(company):
    """Load corpus text for a given company."""
    company = company.lower().strip()
    filename = COMPANY_MAP.get(company)

    if filename is None:
        # Load all corpora for unknown company
        all_text = ""
        for f in ["hackerrank", "claude", "visa"]:
            path = os.path.join(CORPUS_DIR, f"{f}.txt")
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as file:
                    all_text += file.read() + "\n\n"
        return all_text

    path = os.path.join(CORPUS_DIR, f"{filename}.txt")
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def chunk_text(text, chunk_size=20):
    """Split text into overlapping chunks of chunk_size lines."""
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    chunks = []
    for i in range(0, len(lines), chunk_size // 2):
        chunk = lines[i:i + chunk_size]
        if chunk:
            chunks.append("\n".join(chunk))
    return chunks

def score_chunk(chunk, keywords):
    """Score a chunk based on keyword overlap."""
    chunk_lower = chunk.lower()
    score = 0
    for word in keywords:
        if word in chunk_lower:
            score += 1
    return score

def extract_keywords(text):
    """Extract meaningful keywords from ticket text."""
    # Remove common stop words
    stop_words = {
        "i", "me", "my", "we", "our", "you", "your", "the", "a", "an",
        "is", "are", "was", "were", "be", "been", "have", "has", "had",
        "do", "does", "did", "will", "would", "could", "should", "may",
        "can", "to", "of", "in", "on", "at", "for", "with", "about",
        "and", "or", "but", "not", "this", "that", "it", "its", "so",
        "please", "hello", "hi", "thanks", "thank", "need", "want",
        "help", "how", "what", "when", "where", "why", "who"
    }
    words = re.findall(r'\b[a-z]{3,}\b', text.lower())
    return [w for w in words if w not in stop_words]

def retrieve(issue, subject, company, top_k=5):
    """Retrieve top_k most relevant chunks for a given ticket."""
    # Combine issue and subject for keyword extraction
    combined_text = f"{issue} {subject}"
    keywords = extract_keywords(combined_text)

    if not keywords:
        return []

    # Load appropriate corpus
    corpus = load_corpus(company)
    if not corpus:
        return []

    # Chunk and score
    chunks = chunk_text(corpus)
    scored = [(score_chunk(c, keywords), c) for c in chunks]
    scored = [(s, c) for s, c in scored if s > 0]
    scored.sort(key=lambda x: x[0], reverse=True)

    # Return top_k chunks
    return [c for _, c in scored[:top_k]]

if __name__ == "__main__":
    # Quick test
    results = retrieve(
        issue="how do I delete my hackerrank account",
        subject="delete account",
        company="HackerRank",
        top_k=3
    )
    print(f"Found {len(results)} chunks\n")
    for i, chunk in enumerate(results):
        print(f"--- Chunk {i+1} ---")
        print(chunk[:300])
        print()