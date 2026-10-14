import os

from ocr.pdf_to_images import convert_pdf_to_images
from ocr.paddle_ocr import OCRExtractor
from ocr.save_text import save_text

from preprocessing.clean_text import TextCleaner
from preprocessing.chunk_text import TextChunker, save_chunks
from embeddings.embedding_model import (
    EmbeddingGenerator,
    save_embeddings
)
from database.postgres_db import PostgreSQLDatabase



embedding_generator = EmbeddingGenerator()

db = PostgreSQLDatabase()
# =====================================================
# Project Folders
# =====================================================

PDF_FOLDER = "data/pdfs"

IMAGE_FOLDER = "processed/images"

RAW_TEXT_FOLDER = "processed/text"

CLEAN_TEXT_FOLDER = "processed/clean"

CHUNK_FOLDER = "processed/chunks"
EMBEDDING_FOLDER = "processed/embeddings"


# =====================================================
# Chunk Configuration
# =====================================================

CHUNK_SIZE = 500

CHUNK_OVERLAP = 100


# =====================================================
# Test Configuration
# =====================================================

TEST_MODE = True

TEST_FILE = "images.png"


# =====================================================
# Initialize Pipeline
# =====================================================

ocr = OCRExtractor()

cleaner = TextCleaner()

chunker = TextChunker(
    chunk_size=CHUNK_SIZE,
    overlap=CHUNK_OVERLAP
)


# =====================================================
# Load Documents
# =====================================================

if TEST_MODE:

    pdf_files = [TEST_FILE]

else:

    pdf_files = sorted([
        file
        for file in os.listdir(PDF_FOLDER)
        if file.lower().endswith(".pdf")
    ])

print(f"\nFound {len(pdf_files)} PDF(s)\n")


# =====================================================
# Process Documents
# =====================================================

for pdf_file in pdf_files:

    pdf_path = os.path.join(PDF_FOLDER, pdf_file)

    if not os.path.exists(pdf_path):

        print(f"❌ File not found: {pdf_path}")
        continue

    print("=" * 70)
    print(f"Processing document: {pdf_file}")
    print("=" * 70)

    # =================================================
    # STEP 1 - PDF -> Images
    # =================================================

    image_paths = convert_pdf_to_images(
        pdf_path,
        IMAGE_FOLDER
    )

    print(f"✅ {len(image_paths)} page(s) converted to images.")

    # =================================================
    # STEP 2 - OCR
    # =================================================

    full_text = ""

    for page_number, image_path in enumerate(image_paths, start=1):

        print(f"OCR Page {page_number}/{len(image_paths)}")

        page_text = ocr.extract_text(image_path)

        full_text += f"\n\n===== PAGE {page_number} =====\n\n"

        full_text += page_text

    # =================================================
    # STEP 3 - Save Raw OCR
    # =================================================

    txt_filename = os.path.splitext(pdf_file)[0] + ".txt"

    raw_output = save_text(
        full_text,
        RAW_TEXT_FOLDER,
        txt_filename
    )

    print(f"✅ Raw OCR saved:")
    print(f"   {raw_output}")

    # =================================================
    # STEP 4 - Clean OCR Text
    # =================================================

    cleaned_text = cleaner.clean(full_text)

    clean_output = save_text(
        cleaned_text,
        CLEAN_TEXT_FOLDER,
        txt_filename
    )

    print(f"✅ Clean text saved:")
    print(f"   {clean_output}")

    # =================================================
    # STEP 5 - Chunking
    # =================================================

    chunks = chunker.chunk(cleaned_text)

    #
    # Add metadata to every chunk
    #

    for chunk in chunks:

        chunk["document_name"] = pdf_file

    json_filename = os.path.splitext(pdf_file)[0] + ".json"

    chunk_output = save_chunks(
        chunks,
        CHUNK_FOLDER,
        json_filename
    )

    print(f"✅ {len(chunks)} chunk(s) created.")
    print(f"   {chunk_output}")
    # =====================================
    # STEP 6 - Generate Embeddings
    # =====================================

    embeddings = embedding_generator.generate(chunks)

    embedding_filename = (
        os.path.splitext(pdf_file)[0]
        + "_embeddings.json"
    )

    embedding_output = save_embeddings(
        embeddings,
        EMBEDDING_FOLDER,
        embedding_filename
    )

    print(f"✅ {len(embeddings)} embeddings created.")
    print(f"   {embedding_output}")
        # =================================================
    # STEP 7 - Store in PostgreSQL
    # =================================================

    print("Saving data to PostgreSQL...")

    # Insert document
    document_id = db.insert_document(pdf_file)

    # Insert raw OCR text
    db.insert_ocr_text(
        document_id,
        full_text
    )

    # Insert cleaned text
    db.insert_clean_text(
        document_id,
        cleaned_text
    )

    # Insert each chunk and its embedding
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings), start=1):

        chunk_id = db.insert_chunk(
            document_id=document_id,
            chunk_number=i,
            chunk_text=chunk["text"]
        )

        db.insert_embedding(
           chunk_id=chunk_id,
           embedding=embedding["embedding"]
        )
    print("✅ Data successfully stored in PostgreSQL.")

db.close()

print("\n🎉 Pipeline Finished Successfully!")