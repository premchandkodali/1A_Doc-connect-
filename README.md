PDF Outline Extractor
A high-performance, offline-capable solution for extracting structured outlines from PDF documents. This tool identifies titles and headings (H1, H2, H3) along with their page numbers, outputting results in JSON format.
Problem Statement
Extract structured outlines from PDF documents including:

Document title
Hierarchical headings (H1, H2, H3)
Corresponding page numbers
JSON formatted output

Constraints:

Execution time: < 10 seconds for 50-page PDFs
Offline operation (no internet access)
AMD64 CPU compatibility
Docker containerized deployment

Approach
Our solution implements a rule-based system using font analysis and layout detection to identify document structure. The approach focuses on:
Core Strategy

Title Detection: Identifies the largest/rarest font on the first two pages
Heading Classification: Uses statistical font analysis to categorize H1, H2, H3 levels
Layout Analysis: Considers font size, boldness, and vertical positioning
Content Filtering: Excludes form fields, page numbers, and non-content text

Key Heuristics

Body Text Identification: Most common font size serves as baseline
Heading Detection: Rare font sizes (< 20% of total lines) indicate headings
Emphasis Recognition: Bold fonts suggest heading importance
Content Validation: Filters out numbers, short text, and form elements
Multi-language Support: Handles Unicode content including non-English text

Processing Pipeline

Font Analysis: Statistical analysis of all text blocks
Hierarchy Detection: Relative font size comparison for heading levels
Structure Mapping: Builds hierarchical outline with page references
JSON Generation: Outputs structured data in standardized format

Technologies & Libraries
Programming Language

Python 3.10: Core development platform

Key Libraries

PyMuPDF (fitz): PDF parsing and text extraction
collections: Statistical analysis and data structures
json: Output formatting
os: File system operations

Containerization

Docker: Based on python:3.10-slim image
Platform: linux/amd64 architecture support

Installation & Setup
Prerequisites

Docker installed on your system
Input PDF files in designated folder
Output directory for JSON results

Docker Build
bashdocker build --platform linux/amd64 -t dotconnector:v1 .
Directory Structure
project/
├── Dockerfile
├── main.py
├── requirements.txt
├── input/          # Place your PDF files here
└── output/         # JSON outputs will be generated here
Usage
Docker Execution
bashdocker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  dotconnector:v1
Input Requirements

Place PDF files in the input/ directory
Files will be processed automatically
No specific naming convention required

Expected Execution Flow

Container reads all PDF files from /app/input
Processes each PDF using font analysis algorithms
Generates corresponding .json files in /app/output
Completes processing within performance constraints

Output Format
JSON Schema
json{
  "title": "Document Title",
  "outline": [
    {
      "level": "H1",
      "text": "Main Section Heading",
      "page": 1
    },
    {
      "level": "H2",
      "text": "Subsection Heading",
      "page": 2
    },
    {
      "level": "H3",
      "text": "Sub-subsection Heading",
      "page": 2
    }
  ]
}
Output Characteristics

Title: Extracted from first two pages using largest/rarest fonts
Outline: Array of heading objects with hierarchical structure
Levels: Title, H1, H2, H3 based on font size hierarchy
Page Numbers: Zero-indexed page references
Unicode Support: Handles multi-language text properly

Performance Features
Optimization Strategies

Memory Efficiency: Page-by-page processing to minimize RAM usage
Fast Execution: Statistical font analysis reduces processing time
Error Resilience: Continues operation even with problematic files
Batch Processing: Handles multiple PDFs in single execution

Constraint Compliance

✅ Speed: < 10 seconds execution time
✅ Offline: No internet connectivity required
✅ Platform: AMD64 CPU compatibility
✅ Containerized: Full Docker support with network isolation

Multi-language Support
Supported Features

Unicode Text: Handles various character encodings
Non-English Content: Processes Hindi, Arabic, Chinese, etc.
Mixed Languages: Documents with multiple language sections
Special Characters: Mathematical symbols, accented characters

Document Type Compatibility
Supported Formats

Academic Papers: Research documents with standard formatting
Technical Reports: Engineering and scientific documentation
Educational Materials: Textbooks, course materials, presentations
Form Documents: Structured forms with heading hierarchies
Mixed Content: Documents with varied formatting styles

Troubleshooting
Common Issues

Font Detection: Varies by document formatting standards
Heading Recognition: Depends on consistent font usage
Multi-column Layouts: May affect heading sequence
Scanned PDFs: Text-based PDFs work best

Performance Tips

Ensure PDFs contain selectable text (not just images)
Documents with consistent formatting yield better results
Complex layouts may require manual verification

Repository
GitHub: https://github.com/premchandkodali/1A_Doc-connect-
License
This project is developed for the DotConnector challenge and follows the specified technical requirements and constraints.
