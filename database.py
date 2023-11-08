import sqlite3


# Define a function to connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect("./conversation.db.sqlite")
    conn.row_factory = sqlite3.Row
    return conn


# Define a function to create the tables for storing conversations and messages
def create_tables():
    conn = get_db_connection()
    # Create the conversations table
    conn.execute(
        """
    CREATE TABLE IF NOT EXISTS conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """
    )
    # Create the messages table with a foreign key to conversations
    conn.execute(
        """
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        conversation_id INTEGER,
        type TEXT NOT NULL,
        content TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (conversation_id) REFERENCES conversations (id)
    )
    """
    )
    conn.commit()
    conn.close()


# Call the function to create the tables
create_tables()
