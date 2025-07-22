import os
import json
import fitz  # PyMuPDF
import pandas as pd

INPUT_DIR = "input"
GROUND_TRUTH_DIR = "ground_truth_output"  # Directory for your sample JSONs
OUTPUT_CSV = "labeled_lines.csv"

def extract_lines_from_pdf(pdf_path):
    """Extracts all text lines from a PDF, preserving page number."""
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
                    if text:
                        spans.append((span["bbox"][0], text))
                
                if spans:
                    spans.sort()
                    line_text = " ".join([t[1] for t in spans])
                    lines.append({"text": line_text, "page": page_num, "label": "Body"}) # Default to Body
    return lines

def label_data():
    """
    Creates a labeled dataset from PDFs and their corresponding ground truth JSON files.
    """
    labeled_data = []
    pdf_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(".pdf")]

    for pdf_file in pdf_files:
        pdf_path = os.path.join(INPUT_DIR, pdf_file)
        json_file = pdf_file.replace(".pdf", ".json")
        json_path = os.path.join(GROUND_TRUTH_DIR, json_file)

        if not os.path.exists(json_path):
            print(f"Warning: No ground truth JSON found for {pdf_file}. Skipping.")
            continue

        print(f"Processing {pdf_file}...")
        
        # Extract all lines from the PDF
        lines = extract_lines_from_pdf(pdf_path)

        # Load ground truth
        with open(json_path, 'r', encoding='utf-8') as f:
            ground_truth = json.load(f)

        title_text = ground_truth.get("title", "").strip()
        outline_items = ground_truth.get("outline", [])
        
        # Create a quick lookup for headings
        headings = {(item["text"].strip(), item["page"]): item["level"] for item in outline_items}

        # Label the extracted lines
        for line in lines:
            line_text_stripped = line["text"].strip()
            
            # Check if it's the title
            if title_text and title_text in line_text_stripped and line["page"] == 0:
                line["label"] = "Title"
            # Check if it's a heading
            elif (line_text_stripped, line["page"]) in headings:
                line["label"] = headings[(line_text_stripped, line["page"])]
        
        labeled_data.extend(lines)

    # Save to CSV
    df = pd.DataFrame(labeled_data)
    df = df[["text", "label"]] # We only need text and label for training
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"\nSuccessfully created labeled dataset at {OUTPUT_CSV}")
    print(f"Total lines labeled: {len(df)}")
    print("Label distribution:")
    print(df['label'].value_counts())


if __name__ == "__main__":
    label_data() 