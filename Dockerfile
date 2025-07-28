FROM --platform=linux/amd64 python:3.10

# Set working directory
WORKDIR /app

# Install system dependencies for pdfplumber
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir pdfplumber==0.11.4

# Copy the Python script
COPY process_pdfs_part1.py .

# Create input and output directories
RUN mkdir -p /input /output

# Set the entrypoint to run the script
ENTRYPOINT ["python", "process_pdfs_part1.py"]