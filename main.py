import os
import json
import fitz  # PyMuPDF
from collections import Counter, defaultdict
import re

INPUT_DIR = "input"
OUTPUT_DIR = "output"

def cluster_font_sizes(sizes, threshold=0.5):
    sizes = sorted(list(set(sizes)), reverse=True)
    clusters = []
    for size in sizes:
        placed = False
        for cluster in clusters:
            if abs(cluster[0] - size) <= threshold:
                cluster.append(size)
                placed = True
                break
        if not placed:
            clusters.append([size])
    return [sum(cluster)/len(cluster) for cluster in clusters]

def extract_outline(pdf_path):
    doc = fitz.open(pdf_path)
    lines = []
    font_sizes = []

    for page_num, page in enumerate(doc):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                line_text = ""
                line_sizes = []
                line_flags = []
                line_fonts = []
                line_xs = []
                spans = []
                for span in line["spans"]:
                    text = span["text"].strip()
                    if not text or len(text) < 2:
                        continue
                    size = span["size"]
                    font = span["font"]
                    flags = span["flags"]
                    font_sizes.append(size)
                    spans.append((span["bbox"][0], text, size, font, flags))
                if spans:
                    # Sort spans by x coordinate (left to right)
                    spans.sort()
                    line_text = " ".join([t[1] for t in spans])
                    line_sizes = [t[2] for t in spans]
                    line_fonts = [t[3] for t in spans]
                    line_flags = [t[4] for t in spans]
                    lines.append({
                        "text": line_text,
                        "sizes": line_sizes,
                        "fonts": line_fonts,
                        "flags": line_flags,
                        "max_size": max(line_sizes),
                        "any_bold": any(f & 2 for f in line_flags),
                        "page": page_num
                    })

    # Cluster font sizes
    clustered_sizes = cluster_font_sizes(font_sizes)
    size_counts = Counter([round(s, 1) for s in font_sizes])
    body_size = size_counts.most_common(1)[0][0]
    heading_sizes = [s for s in clustered_sizes if s > body_size + 0.1]
    h_sizes = heading_sizes[:3]
    h_levels = {}
    for i, h in enumerate(h_sizes):
        h_levels[round(h, 1)] = f"H{i+1}"

    # Title: largest text on first page, not a header/footer, not too short
    title = ""
    first_page_lines = [l for l in lines if l["page"] == 1]
    if first_page_lines:
        candidates = [l for l in first_page_lines if len(l["text"]) > 5 and not l["text"].isupper()]
        if candidates:
            title_line = max(candidates, key=lambda l: l["max_size"])
            title = title_line["text"]

    outline = []
    for l in lines:
        size_rounded = round(l["max_size"], 1)
        is_heading = False
        level = None
        if size_rounded in h_levels:
            is_heading = True
            level = h_levels[size_rounded]
        elif l["any_bold"] and l["max_size"] > body_size:
            is_heading = True
            level = "H3"
        elif re.match(r"^\d+(\.\d+)*\s", l["text"]):
            if l["max_size"] > body_size:
                is_heading = True
                level = "H3"
        if is_heading and level:
            outline.append({
                "level": level,
                "text": l["text"],
                "page": l["page"]
            })

    return {
        "title": title,
        "outline": outline
    }

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for filename in os.listdir(INPUT_DIR):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(INPUT_DIR, filename)
            result = extract_outline(pdf_path)
            output_path = os.path.join(OUTPUT_DIR, filename.replace(".pdf", ".json"))
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"Processed {filename} -> {output_path}")

if __name__ == "__main__":
    main()
