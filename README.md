# PDF Outline Extraction for Challenge 1a

## Overview
This project provides a Python-based solution for extracting document outlines and titles from PDF files, as part of **Challenge 1a: PDF Outline Extraction**. The script processes PDFs in the `input` directory, generates JSON files with titles and outlines, and saves them to the `output` directory. It is designed to run offline, meet a runtime constraint of < 10 seconds, and produce a Docker image < 200 MB, compatible with AMD64 CPU-only hardware.

The solution handles both structured documents (e.g., with hierarchical headings) and form-like PDFs (e.g., with numbered fields), accurately extracting titles and outlines as shown in the expected outputs for `file01.pdf`, `file02.pdf`, `file03.pdf`, and `file04.pdf`.

## Prerequisites
- **Docker**: Required to build and run the container.
- **Input PDFs**: Place PDF files (e.g., `file01.pdf`, `file02.pdf`, `file03.pdf`, `file04.pdf`) in an `input` directory.
- **Hardware**: AMD64 CPU (no GPU required).
- **Operating System**: Linux, macOS, or Windows with Docker support.

## Directory Structure
```
part1/
├── Dockerfile
├── process_pdfs_part1.py
├── input/
│   ├── file01.pdf
│   ├── file02.pdf
│   ├── file03.pdf
│   ├── file04.pdf
│   └── (other PDFs)
├── output/
│   ├── file01.json
│   ├── file02.json
│   ├── file03.json
│   ├── file04.json
│   └── (other JSON outputs)
└── README.md
```

## Dependencies
- **Python**: 3.11
- **pdfplumber**: 0.11.4 (installed in Docker image)

## Installation
1. **Clone or Set Up Repository**:
   - Ensure `Dockerfile`, `process_pdfs_part1.py`, and an `input` directory with PDFs are in the project root (`part1/`).

2. **Build the Docker Image**:
   ```bash
   cd part1
   docker build -t pdf-outline-extractor .
   ```
   - This creates a Docker image (~160 MB) with `python:3.11-slim` and `pdfplumber==0.11.4`.

3. **Prepare Input PDFs**:
   - Place PDF files in the `input` directory (e.g., `part1/input/file01.pdf`).

## Usage
1. **Run the Docker Container**:
   ```bash
   docker run --rm \
     -v $(pwd)/input:/input \
     -v $(pwd)/output:/output \
     pdf-outline-extractor
   ```
   - `--rm`: Removes the container after execution.
   - `-v $(pwd)/input:/input`: Mounts the local `input` directory to `/input` in the container.
   - `-v $(pwd)/output:/output`: Mounts the local `output` directory to `/output` in the container.
   - The script processes all PDFs in `/input` and saves JSON files to `/output`.

2. **Output**:
   - JSON files (e.g., `output/file01.json`) are generated with the following structure:
     ```json
     {
       "title": "Document Title",
       "outline": [
         {
           "level": "H1",
           "text": "Heading Text",
           "page": 1
         },
         ...
       ]
     }
     ```
   - Example for `file01.pdf`:
     ```json
     {
       "title": "Application form for grant of LTC advance",
       "outline": []
     }
     ```

3. **Verify Outputs**:
   - Check the `output` directory for JSON files.
   - Ensure outputs match expected formats (e.g., `file01.json` has an empty outline, `file03.json` has 38 headings).
   - Console logs show:
     - “Generated outline: /output/fileXX.json” for each PDF.
     - “Total runtime: X.XX seconds” (should be < 10 seconds).

## Constraints Met
- **Runtime**: < 10 seconds for processing multiple PDFs (e.g., `file01.pdf`, `file02.pdf`, `file03.pdf`, `file04.pdf`).
- **Model Size**: Docker image is ~160 MB (< 200 MB).
- **Offline**: No external APIs or network calls; all processing is local.
- **Hardware**: Compatible with AMD64 CPU-only systems.
- **Output Format**: JSON files with title and outline, matching expected structures.

## Troubleshooting
1. **Build Fails**:
   - Ensure `process_pdfs_part1.py` and `Dockerfile` are in the project root.
   - Check Docker logs for errors (e.g., missing `pdfplumber`).
   - Run `docker images` to verify image size (~160 MB).

2. **Incorrect Outputs**:
   - Compare JSON files in `output` with expected outputs.
   - For `file01.json`, ensure `outline: []` and title is "Application form for grant of LTC advance".
   - Share incorrect JSONs and logs for debugging.

3. **Runtime Exceeds 10 Seconds**:
   - Share console logs with runtime and system specs (CPU cores, RAM).
   - Optimize script by limiting processed lines if needed.

4. **No Output Files**:
   - Ensure `input` directory contains valid PDFs.
   - Verify volume mounts (`-v`) use absolute paths.
   - Check container logs for errors (e.g., `Error processing fileXX.pdf`).

## Notes
- **Generalizability**: The script handles both form-like PDFs (e.g., `file01.pdf` with no headings) and structured documents (e.g., `file03.pdf` with nested headings).
- **Submission**: Include `Dockerfile`, `process_pdfs_part1.py`, `requirements.txt` (below), and this `README.md` in the submission.
- **requirements.txt**:
  ```text
  pdfplumber==0.11.4
  ```

## Contact
For issues or questions, please provide:
- Console logs from Docker run.
- Output JSON files (e.g., `output/file01.json`).
- System specs (CPU cores, RAM).
- Any additional PDFs for testing.