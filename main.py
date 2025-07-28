import os
import fitz  # PyMuPDF
import json
from collections import Counter, defaultdict

INPUT_DIR = 'input'
OUTPUT_DIR = 'output'

# Heuristic: Use font size and font weight to classify headings
HEADING_LEVELS = ['Title', 'H1', 'H2', 'H3']


def extract_lines_with_fonts(pdf_path):
    doc = fitz.open(pdf_path)
    lines = []
    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")['blocks']
        for block in blocks:
            if block['type'] != 0:
                continue
            for line in block['lines']:
                line_text = " ".join([span['text'] for span in line['spans']]).strip()
                if not line_text:
                    continue
                # Use the largest font size in the line (usually heading)
                max_font_size = max(span['size'] for span in line['spans'])
                # Use the most common font name in the line
                font_names = [span['font'] for span in line['spans']]
                font_name = Counter(font_names).most_common(1)[0][0]
                is_bold = any('Bold' in fn or 'bold' in fn for fn in font_names)
                lines.append({
                    'text': line_text,
                    'page': page_num - 1,  # page numbers start from 0
                    'font_size': max_font_size,
                    'font_name': font_name,
                    'is_bold': is_bold
                })
    return lines


def assign_heading_levels(lines):
    # Count font size frequencies
    font_size_counts = Counter(line['font_size'] for line in lines)
    total_lines = len(lines)
    body_font_size, _ = font_size_counts.most_common(1)[0]
    rare_font_sizes = [size for size, count in font_size_counts.items() if count / total_lines < 0.2]
    rare_font_sizes = sorted(rare_font_sizes, reverse=True)
    size_to_level = {}
    for i, size in enumerate(rare_font_sizes[:len(HEADING_LEVELS)]):
        size_to_level[size] = HEADING_LEVELS[i]
    outline = []
    title_lines = []
    for line in lines:
        if line['font_size'] == body_font_size:
            continue
        level = size_to_level.get(line['font_size'])
        if not level:
            continue
        text = line['text'].strip()
        if len(text) <= 3 or text.replace('.', '').isdigit():
            continue
        skip_patterns = {'s.no', 'name', 'age', 'date', 'rs.', 'signature'}
        if text.lower() in skip_patterns:
            continue
        # Only consider title from first page
        if level == 'Title' and line['page'] == 0 or line['page'] == 1 :
            title_lines.append(text)
        elif level != 'Title':
            entry = {
                'level': level,
                'text': text,
                'page': line['page']
            }
            outline.append(entry)
    # Title only from first page, else empty string
    title = ' '.join(title_lines) if title_lines else ""
    return title, outline


def process_pdf(pdf_path, out_path):
    lines = extract_lines_with_fonts(pdf_path)
    title, outline = assign_heading_levels(lines)
    result = {
        'title': title,
        'outline': outline
    }
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pdf_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith('.pdf')]
    for pdf_file in pdf_files:
        pdf_path = os.path.join(INPUT_DIR, pdf_file)
        out_file = os.path.splitext(pdf_file)[0] + '.json'
        out_path = os.path.join(OUTPUT_DIR, out_file)
        print(f"Processing {pdf_file} ...")
        process_pdf(pdf_path, out_path)
        print(f"  -> Saved outline to {out_file}")

if __name__ == '__main__':
    main()