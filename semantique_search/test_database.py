from database.postgres_db import PostgreSQLDatabase

db = PostgreSQLDatabase()

query = """
SELECT filename
FROM documents;
"""

results = db.fetch_all(query)

print(results)

db.close()