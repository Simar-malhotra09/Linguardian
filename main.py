import argparse
from linguardian.linguardian import Linguardian

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Extract OCR text from a PDF and blur English words.")
    parser.add_argument('--file', type=str, required=True, help='Path to the input PDF file')
    parser.add_argument('--output', type=str, required=True, help='Path to save the OCR output text file')

    args = parser.parse_args()

    # Create an instance of PDFTextBlurrer and process the PDF
    blurrer = Linguardian(args.file, args.output)
    blurrer.process_pdf()


if __name__ == "__main__":
    main()
