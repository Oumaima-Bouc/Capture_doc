from paddleocr import PaddleOCR


class OCRExtractor:

    def __init__(self, language="en"):

        self.ocr = PaddleOCR(
            use_angle_cls=True,
            lang=language
        )

    def extract_text(self, image_path):

        result = self.ocr.predict(image_path)

        if not result:
            return ""

        page = result[0]

        texts = page["rec_texts"]

        return "\n".join(texts)