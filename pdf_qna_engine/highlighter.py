import io
import pdfplumber
from typing import List, Optional

def find_highlight_coords(pdf_bytes: bytes, answer: str) -> Optional[List[dict]]:
    """
    Search for the answer text in the PDF and return
    highlight annotations with page number and bounding box.
    """
    if not answer or len(answer.strip()) < 3:
        return None

    highlights = []

    # Clean answer for matching — take first sentence only
    search_text = answer.split(".")[0].strip().lower()

    # Use a sliding window of words to find the best matching span
    search_words = search_text.split()
    window_size = min(len(search_words), 6)  # match up to 6 words

    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            words = page.extract_words()
            if not words:
                continue

            page_words = [w["text"].lower() for w in words]

            # Slide window across page words looking for a match
            for i in range(len(page_words) - window_size + 1):
                window = " ".join(page_words[i:i + window_size])
                query  = " ".join(search_words[:window_size])

                # Check similarity — allow partial match
                matching = sum(
                    1 for a, b in zip(window.split(), query.split()) if a == b
                )
                match_ratio = matching / window_size

                if match_ratio >= 0.6:  # 60% word overlap threshold
                    matched_words = words[i:i + window_size]

                    # Build bounding box around matched words
                    x0 = min(w["x0"] for w in matched_words)
                    y0 = min(w["top"] for w in matched_words)
                    x1 = max(w["x1"] for w in matched_words)
                    y1 = max(w["bottom"] for w in matched_words)

                    highlights.append({
                        "page": page_num,
                        "x0": x0,
                        "y0": y0,
                        "x1": x1,
                        "y1": y1,
                    })
                    break  # one highlight per page is enough

    return highlights if highlights else None