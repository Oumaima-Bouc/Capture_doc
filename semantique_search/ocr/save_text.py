import os


def save_text(text, output_folder, filename):
    """
    Save extracted OCR text into a .txt file.
    """

    os.makedirs(output_folder, exist_ok=True)

    output_path = os.path.join(output_folder, filename)

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(text)

    return output_path