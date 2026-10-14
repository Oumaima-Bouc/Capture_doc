import psycopg2


class PostgreSQLDatabase:

    def __init__(
        self,
        database="semantic_search",
        user="macbook",
        password="",
        host="localhost",
        port="5432"
    ):

        self.connection = psycopg2.connect(
            database=database,
            user=user,
            password=password,
            host=host,
            port=port
        )

        self.cursor = self.connection.cursor()

    # ------------------------------------------
    # Close connection
    # ------------------------------------------

    def close(self):

        self.cursor.close()
        self.connection.close()

    # ------------------------------------------
    # Insert document
    # ------------------------------------------

    def insert_document(self, filename):

        query = """
        INSERT INTO documents(filename)
        VALUES (%s)
        RETURNING id;
        """

        self.cursor.execute(query, (filename,))

        document_id = self.cursor.fetchone()[0]

        self.connection.commit()

        return document_id

    # ------------------------------------------
    # Insert OCR text
    # ------------------------------------------

    def insert_ocr_text(self, document_id, raw_text):

        query = """
        INSERT INTO ocr_text(document_id, raw_text)
        VALUES (%s, %s);
        """

        self.cursor.execute(
            query,
            (
                document_id,
                raw_text
            )
        )

        self.connection.commit()

    # ------------------------------------------
    # Insert Clean Text
    # ------------------------------------------

    def insert_clean_text(self, document_id, clean_text):

        query = """
        INSERT INTO clean_text(document_id, clean_text)
        VALUES (%s, %s);
        """

        self.cursor.execute(
            query,
            (
                document_id,
                clean_text
            )
        )

        self.connection.commit()

    # ------------------------------------------
    # Insert Chunk
    # ------------------------------------------

    def insert_chunk(
        self,
        document_id,
        chunk_number,
        chunk_text
    ):

        query = """
        INSERT INTO chunks
        (
            document_id,
            chunk_number,
            chunk_text
        )
        VALUES
        (
            %s,
            %s,
            %s
        )
        RETURNING id;
        """

        self.cursor.execute(
            query,
            (
                document_id,
                chunk_number,
                chunk_text
            )
        )

        chunk_id = self.cursor.fetchone()[0]

        self.connection.commit()

        return chunk_id

    # ------------------------------------------
    # Insert Embedding
    # ------------------------------------------

    def insert_embedding(
        self,
        chunk_id,
        embedding
    ):

        vector = "[" + ",".join(map(str, embedding)) + "]"

        query = """
        INSERT INTO embeddings
        (
            chunk_id,
            embedding
        )
        VALUES
        (
            %s,
            %s
        );
        """

        self.cursor.execute(
            query,
            (
                chunk_id,
                vector
            )
        )

        self.connection.commit()


    # ------------------------------------------
    # Execute SELECT query
    # ------------------------------------------

    def fetch_all(self, query, params=None):

        self.cursor.execute(query, params)

        return self.cursor.fetchall()