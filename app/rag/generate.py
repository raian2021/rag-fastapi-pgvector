def generate_answer(question: str, contexts: list[dict]) -> dict:
    if not contexts:
        return {
            "answer": "No relevant information found.",
            "citations": [],
        }

    top = contexts[:3]
    citations = []
    evidence_lines = []

    for i, c in enumerate(top, start=1):
        citations.append({
            "ref": f"[{i}]",
            "source": c["source"],
            "chunk_index": c["chunk_index"],
            "score": round(c["score"], 4),
        })

        snippet = c["content"].strip().replace("\n", " ")
        snippet = snippet[:280] + ("..." if len(snippet) > 280 else "")
        evidence_lines.append(f"[{i}] {snippet}")

    answer = (
        "Based on retrieved evidence:\n\n"
        + "\n".join(evidence_lines)
    )

    return {
        "answer": answer,
        "citations": citations,
    }

