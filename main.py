import os
import json
import fitz
from sentence_transformers import SentenceTransformer
from joblib import load

INPUT_DIR = "input"
OUTPUT_DIR = "output"
SVM_MODEL_PATH = "svm_headings.joblib"

def extract_lines(pdf_path):
    doc = fitz.open(pdf_path)
    lines = []
    for page_num, page in enumerate(doc):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                spans = []
                for span in line["spans"]:
                    text = span["text"].strip()
                    if not text or len(text) < 2:
                        continue
                    spans.append((span["bbox"][0], text))
                if spans:
                    spans.sort()
                    line_text = " ".join([t[1] for t in spans])
                    lines.append({
                        "text": line_text,
                        "page": page_num  # 0-based
                    })
    return lines

def classify_lines(lines, model, clf, le):
    texts = [l["text"] for l in lines]
    embeddings = model.encode(texts, show_progress_bar=False)
    preds = clf.predict(embeddings)
    labels = le.inverse_transform(preds)
    for i, l in enumerate(lines):
        l["label"] = labels[i]
    return lines

def build_outline(lines):
    title = ""
    outline = []
    for l in lines:
        if l["label"] == "Title" and not title:
            title = l["text"]
        elif l["label"] in {"H1", "H2", "H3"}:
            outline.append({
                "level": l["label"],
                "text": l["text"],
                "page": l["page"]
            })
    return {"title": title, "outline": outline}

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    model = SentenceTransformer('all-MiniLM-L6-v2')
    clf, le = load(SVM_MODEL_PATH)
    for filename in os.listdir(INPUT_DIR):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(INPUT_DIR, filename)
            lines = extract_lines(pdf_path)
            lines = classify_lines(lines, model, clf, le)
            result = build_outline(lines)
            output_path = os.path.join(OUTPUT_DIR, filename.replace(".pdf", ".json"))
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"Processed {filename} -> {output_path}")

if __name__ == "__main__":
    main()
