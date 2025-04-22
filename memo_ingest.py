from drive_client import get_memo_files, get_docs_service
from embedding import store_memo_in_vector_store
import mysql.connector
import os

# MySQL database connection config (set via environment variables in Render)
DB_CONFIG = {
    'host': os.getenv("DB_HOST", "localhost"),
    'user': os.getenv("DB_USER", "root"),
    'password': os.getenv("DB_PASSWORD", ""),
    'database': os.getenv("DB_NAME", "memo_db")
}

def ingest_file(file, user_id):
    docs_service = get_docs_service()
    file_id = file['id']
    name = file['name']
    mime_type = file['mimeType']
    last_modified = file['modifiedTime']
    content = ""

    if mime_type == 'application/vnd.google-apps.document':
        doc = docs_service.documents().get(documentId=file_id).execute()
        content = "\n".join([
            elem.get('textRun', {}).get('content', '')
            for elem in doc.get('body', {}).get('content', [])
            if 'textRun' in elem.get('paragraph', {})
        ])
    else:
        return None

    # Save to MySQL
    try:
        db = mysql.connector.connect(**DB_CONFIG)
        cursor = db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memo_files (
                id VARCHAR(255) PRIMARY KEY,
                name TEXT,
                content LONGTEXT,
                last_modified DATETIME,
                mime_type VARCHAR(255),
                user_id VARCHAR(255)
            )
        """)
        cursor.execute("""
            INSERT INTO memo_files (id, name, content, last_modified, mime_type, user_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE content=%s, last_modified=%s
        """, (
            file_id, name, content, last_modified, mime_type, user_id,
            content, last_modified
        ))
        db.commit()
        cursor.close()
        db.close()
    except Exception as e:
        print("DB error:", e)

    # Store in vector DB
    store_memo_in_vector_store(
        doc_id=file_id,
        title=name,
        content=content,
        user_id=user_id,
        last_modified=last_modified
    )

    return name

def sync_drive_memos(user_id):
    files = get_memo_files()
    updated = []
    for file in files:
        result = ingest_file(file, user_id)
        if result:
            updated.append(result)
    return updated
