# extractor.py
import fitz  # PyMuPDF
import os
import json

def is_heading(text, font_size, font_flags):
    # Heuristic: bold or larger fonts are headings
    return font_size >= 12 and font_flags in [20, 21, 22, 23]

def get_heading_level(font_size, heading_sizes):
    if font_size == heading_sizes[0]:
        return "H1"
    elif font_size == heading_sizes[1]:
        return "H2"
    else:
        return "H3"

def extract_outline(pdf_path):
    doc = fitz.open(pdf_path)
    title = os.path.basename(pdf_path).replace(".pdf", "")
    headings = []

    font_sizes = set()
    elements = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    text = ""
                    for span in line["spans"]:
                        font_size = round(span["size"])
                        font_flags = span["flags"]
                        text = span["text"].strip()

                        if len(text) > 3:
                            font_sizes.add(font_size)
                            elements.append((text, font_size, font_flags, page_num + 1))

    # Determine top 3 font sizes as heading levels
    top_sizes = sorted(font_sizes, reverse=True)[:3]

    for text, font_size, font_flags, page_num in elements:
        if is_heading(text, font_size, font_flags):
            level = get_heading_level(font_size, top_sizes)
            headings.append({
                "level": level,
                "text": text,
                "page": page_num
            })

    return {
        "title": title,
        "outline": headings
    }

def main():
    input_dir = "/app/input"
    output_dir = "/app/output"

    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf"):
            input_path = os.path.join(input_dir, filename)
            result = extract_outline(input_path)

            output_filename = filename.replace(".pdf", ".json")
            with open(os.path.join(output_dir, output_filename), "w") as f:
                json.dump(result, f, indent=4)

if __name__ == "__main__":
    main()
