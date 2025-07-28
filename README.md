# Document Structure Extraction - Round 1A

A high-performance, offline-capable system for extracting structured outlines from PDF documents. This solution analyzes document layout and typography to identify titles and hierarchical headings (H1, H2, H3) with precise page number mapping, outputting results in standardized JSON format.

## 🎯 Problem Statement

Extract structured outlines from PDF documents including:
- Document title identification
- Hierarchical heading detection (H1, H2, H3)
- Accurate page number mapping
- JSON format output
- Sub-10 second execution on 50-page PDFs
- Offline operation in containerized environment

## 🏗️ System Architecture

### Core Processing Pipeline

1. **Document Analysis Engine**
   - PyMuPDF-based PDF parsing with layout preservation
   - Font property analysis (size, weight, style)
   - Statistical text classification

2. **Title Extraction Module**
   - Largest font size detection on first two pages
   - Rare font pattern identification
   - Content filtering for accuracy

3. **Heading Classification System**
   - Multi-level hierarchy detection (H1, H2, H3)
   - Relative font size analysis
   - Bold text emphasis recognition

4. **Output Generation**
   - Structured JSON formatting
   - Unicode text support
   - Page number indexing (zero-based)

## 🧠 Intelligence Heuristics

### Font Analysis Strategy
- **Body Text Identification**: Most common font size across document
- **Heading Detection**: Font sizes appearing in <20% of total lines
- **Title Recognition**: Largest/rarest fonts on opening pages
- **Emphasis Detection**: Bold formatting indicates structural importance

### Content Filtering Rules
- Excludes form fields and input elements
- Removes standalone numbers and page references
- Filters short text fragments (<threshold characters)
- Ignores repetitive footer/header content

### Statistical Classification
- Font size frequency analysis for body text baseline
- Relative size thresholds for heading hierarchy
- Position-based importance weighting
- Multi-language text handling

## 🛠️ Technologies & Libraries

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| Runtime | Python | 3.10 | Core processing environment |
| PDF Engine | PyMuPDF | Latest | Document parsing and analysis |
| Data Handling | json | Built-in | Output formatting |
| File Operations | os | Built-in | Directory and file management |
| Statistics | collections | Built-in | Font frequency analysis |
| Container | Docker | Latest | Isolated execution environment |

## 🚀 Quick Start

### Prerequisites
- Docker installed and running
- AMD64/x86_64 architecture
- Input PDF files ready

### Build Container
```bash
docker build --platform linux/amd64 -t dotconnector:v1 .
```

### Prepare Directory Structure
```
project-root/
├── input/           # Place PDF files here
│   ├── document1.pdf
│   ├── document2.pdf
│   └── ...
├── output/          # JSON outputs generated here
├── main.py          # Core processing script
├── Dockerfile       # Container configuration
└── README.md        # This documentation
```

### Execute Processing
```bash
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  dotconnector:v1
```

### Expected Behavior
- Processes all PDF files in `/app/input`
- Generates corresponding `.json` files in `/app/output`
- Maintains original filename with `.json` extension
- Completes processing within 10 seconds per 50-page document

## 📊 Output Format

### JSON Schema Structure
```json
{
  "title": "Document Title Text",
  "outline": [
    {
      "level": "H1",
      "text": "Heading Text",
      "page": 0
    },
    {
      "level": "H2", 
      "text": "Sub-heading Text",
      "page": 1
    }
  ]
}
```

### Output Characteristics
- **Title Field**: Document title from first two pages
- **Outline Array**: Ordered list of headings
- **Level Classification**: Title, H1, H2, H3 hierarchy
- **Page Numbers**: Zero-indexed page references
- **Text Content**: Clean, filtered heading text
- **Unicode Support**: Multi-language compatibility

## ⚡ Performance Specifications

### Execution Constraints
| Metric | Specification |
|--------|---------------|
| Processing Time | <10 seconds (50-page PDF) |
| Platform Support | AMD64/x86_64 CPU |
| Internet Dependency | None (offline operation) |
| Memory Usage | Optimized page-by-page processing |
| Container Size | Minimal footprint |

### Scalability Features
- **Batch Processing**: Handles multiple PDFs simultaneously
- **Memory Efficiency**: Page-by-page analysis prevents overflow
- **Error Resilience**: Continues processing despite individual file issues
- **Resource Optimization**: Minimal CPU and memory footprint

## 🔧 Advanced Capabilities

### Multi-Language Support
- Unicode text extraction and preservation
- Non-English content handling (Hindi, Arabic, etc.)
- Character encoding normalization
- Font analysis across different writing systems

### Document Type Adaptability
- Academic papers and research documents
- Business reports and presentations
- Educational materials and textbooks
- Form-based documents with mixed content
- Technical manuals and specifications

### Robust Content Analysis
- Statistical font size distribution analysis
- Context-aware heading detection
- Structural pattern recognition
- Adaptive threshold calculation

## 🐳 Docker Configuration

### Container Specifications
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py .
CMD ["python", "main.py"]
```

### Volume Mapping
- Input: `$(pwd)/input:/app/input`
- Output: `$(pwd)/output:/app/output`
- Network: `--network none` (offline operation)

## 🔍 Troubleshooting

### Common Issues
- **No Output Generated**: Verify PDF files in input directory
- **Slow Processing**: Check document size and complexity
- **Encoding Errors**: Ensure UTF-8 compatible file names
- **Container Issues**: Verify Docker platform compatibility

### Debug Information
- Processing logs available in container output
- Error messages indicate specific file issues
- Performance metrics displayed during execution

## 📁 Project Structure
```
1A_Doc-connect/
├── main.py              # Core extraction logic
├── Dockerfile           # Container configuration
├── requirements.txt     # Python dependencies
├── README.md           # This documentation
├── approach_explanation.md # Methodology details
├── input/              # PDF input directory
└── output/             # JSON output directory
```
