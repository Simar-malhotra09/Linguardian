from pdf2image import convert_from_path
import os

def save_pdf_as_images(pdf_path: str, output_dir: str, dpi: int = 300) -> list:
    """
    Convert a PDF file to images and save them in the specified directory.
    
    Args:
        pdf_path (str): Path to the PDF file to be converted.
        output_dir (str): Directory to save the resulting images.
        dpi (int): DPI resolution for the output images (default is 300).
    
    Returns:
        list: A list of file paths to the saved images.
    """
    
    os.makedirs(output_dir, exist_ok=True)
    images = convert_from_path(pdf_path, dpi=dpi)
    
    saved_image_paths = []
    for i, image in enumerate(images):
        output_path = os.path.join(output_dir, f"page_{i + 1}.png")
        image.save(output_path, "PNG")
        saved_image_paths.append(output_path)

    return saved_image_paths
