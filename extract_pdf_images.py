import sys
import os
try:
    from pypdf import PdfReader
except ImportError:
    print("MISSING_LIB")
    sys.exit(1)

def extract_images(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        count = 0
        for page_num, page in enumerate(reader.pages):
            for image_file_object in page.images:
                with open(str(count) + image_file_object.name, "wb") as fp:
                    fp.write(image_file_object.data)
                    print(f"Extracted: {count}{image_file_object.name} from page {page_num + 1}")
                count += 1
    except Exception as e:
        print(f"Error extracting images: {e}")

if __name__ == "__main__":
    extract_images("semi-final.pdf")
