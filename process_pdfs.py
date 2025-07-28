import pdfplumber
import json
import os
from pathlib import Path
import re
from statistics import median

def extract_text_elements(pdf_path):
    elements = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            for char in page.chars:
                elements.append({
                    "text": char["text"],
                    "size": char["size"],
                    "font": char["fontname"].lower(),
                    "x0": char["x0"],
                    "y0": char["y0"],
                    "page": page_num,
                    "bold": "bold" in char["fontname"].lower()
                })
            tables = page.find_tables()
            table_bboxes = [t.bbox for t in tables] if tables else []
            elements[-len(page.chars):] = [
                {**e, "in_table": any(in_bbox(e["x0"], e["y0"], tb) for tb in table_bboxes)}
                for e in elements[-len(page.chars):]
            ]
    return elements

def in_bbox(x, y, bbox):
    x0, y0, x1, y1 = bbox
    return x0 <= x <= x1 and y0 <= y <= y1

def group_into_lines(elements):
    lines = []
    current_line = []
    elements.sort(key=lambda e: (e["page"], e["y0"], e["x0"]))
    for elem in elements:
        if not current_line or (
            elem["page"] == current_line[-1]["page"] and
            abs(elem["y0"] - current_line[-1]["y0"]) < 2
        ):
            current_line.append(elem)
        else:
            lines.append(current_line)
            current_line = [elem]
    if current_line:
        lines.append(current_line)
    return [
        {
            "text": "".join(e["text"] for e in line).strip(),
            "size": median([e["size"] for e in line]),
            "bold": any(e["bold"] for e in line),
            "x0": min(e["x0"] for e in line),
            "page": line[0]["page"],
            "in_table": any(e["in_table"] for e in line)
        }
        for line in lines if "".join(e["text"] for e in line).strip()
    ]

def calculate_median_font_size(elements):
    font_sizes = [e["size"] for e in elements]
    return median(font_sizes) if font_sizes else 12

def classify_headings(lines, median_font_size):
    headings = []
    numbered_pattern = re.compile(r"^\d+(\.\d+)*\.?\s")
    for line in lines:
        if line["in_table"]:
            continue
        text = line["text"]
        is_numbered = bool(numbered_pattern.match(text))
        is_large = line["size"] > median_font_size
        is_short = len(text.split()) < 15
        is_left_aligned = line["x0"] < 100
        is_bold = line["bold"]
        if (is_numbered or is_large or is_bold) and is_short and is_left_aligned:
            headings.append(line)
    return headings

def determine_levels(headings):
    numbered_pattern = re.compile(r"^(\d+(\.\d+)*)\.?\s")
    font_sizes = sorted(set(h["size"] for h in headings), reverse=True)
    size_to_level = {size: f"H{min(i+1, 3)}" for i, size in enumerate(font_sizes[:3])}
    for h in headings:
        match = numbered_pattern.match(h["text"])
        if match:
            level = len(match.group(1).split("."))
            h["level"] = f"H{min(level, 3)}"
        else:
            h["level"] = size_to_level.get(h["size"], "H1")

def extract_title(headings):
    page1_headings = [h for h in headings if h["page"] == 1]
    if not page1_headings:
        return "Unknown Title"
    largest = max(page1_headings, key=lambda h: h["size"])
    return largest["text"]

def process_pdf(pdf_path, output_path):
    elements = extract_text_elements(pdf_path)
    if not elements:
        return
    lines = group_into_lines(elements)
    median_font_size = calculate_median_font_size(elements)
    headings = classify_headings(lines, median_font_size)
    determine_levels(headings)
    title = extract_title(headings)
    outline = [{"level": h["level"], "text": h["text"], "page": h["page"]} for h in headings]
    with open(output_path, "w") as f:
        json.dump({"title": title, "outline": outline}, f, indent=2)

def main():
    input_dir = Path("input")
    output_dir = Path("output")
    os.makedirs(output_dir, exist_ok=True)
    for pdf_file in input_dir.glob("*.pdf"):
        output_file = output_dir / f"{pdf_file.stem}.json"
        try:
            process_pdf(str(pdf_file), str(output_file))
        except Exception as e:
            print(f"Error processing {pdf_file}: {e}")

if __name__ == "__main__":
    main()