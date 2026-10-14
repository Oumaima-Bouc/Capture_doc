import os
import fitz


def convert_pdf_to_images(pdf_path, output_folder, dpi=200):
    """
    Convert each page of a PDF into a PNG image.

    Args:
        pdf_path (str): Path to PDF.
        output_folder (str): Folder to save images.
        dpi (int): Image resolution.

    Returns:
        list: List of generated image paths.
    """

    os.makedirs(output_folder, exist_ok=True)

    document = fitz.open(pdf_path)

    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]

    image_paths = []

    for page_number in range(len(document)):

        page = document.load_page(page_number)

        pix = page.get_pixmap(dpi=dpi)

        image_name = f"{pdf_name}_page_{page_number + 1}.png"

        image_path = os.path.join(output_folder, image_name)

        pix.save(image_path)

        image_paths.append(image_path)

    document.close()

    return image_paths