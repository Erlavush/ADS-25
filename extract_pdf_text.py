import sys
try:
    from pypdf import PdfReader
except ImportError:
    print("MISSING_LIB")
    sys.exit(1)

try:
    reader = PdfReader("semi-final.pdf")
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    
    with open("pdf_content.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print("Done writing to pdf_content.txt")
except Exception as e:
    print(f"Error reading PDF: {e}")
