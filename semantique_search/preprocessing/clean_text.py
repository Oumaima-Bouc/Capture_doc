import re
import unicodedata


class TextCleaner:
    """
    Cleans OCR text while preserving important information
    for semantic search.
    """

    def clean(self, text: str) -> str:

        # ----------------------------
        # 1. Normalize Unicode
        # ----------------------------
        text = unicodedata.normalize("NFKC", text)

        # ----------------------------
        # 2. Replace tabs with spaces
        # ----------------------------
        text = text.replace("\t", " ")

        # ----------------------------
        # 3. Remove trailing spaces
        # ----------------------------
        text = re.sub(r"[ ]+", " ", text)

        # ----------------------------
        # 4. Remove spaces before newline
        # ----------------------------
        text = re.sub(r" +\n", "\n", text)

        # ----------------------------
        # 5. Collapse many blank lines
        # ----------------------------
        text = re.sub(r"\n{3,}", "\n\n", text)

        # ----------------------------
        # 6. Remove page numbers
        # Example:
        #
        # 1
        #
        # ===== PAGE 2 =====
        #
        # becomes
        #
        # ===== PAGE 2 =====
        # ----------------------------
        text = re.sub(
            r"\n\d+\n(?=\n?===== PAGE)",
            "\n",
            text
        )

        # ----------------------------
        # 7. Strip beginning/end
        # ----------------------------
        text = text.strip()

        return text