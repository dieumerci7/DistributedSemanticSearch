import psycopg2
import json
from tqdm import tqdm

# Database connection parameters
db_params = {
    'host': 'localhost',
    'port': 5432,
    'database': 'arxiv_database',
    'user': 'arxiv_user',
    'password': 'arxiv_password',
}


def create_papers_table(cursor):
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS papers (
        id SERIAL PRIMARY KEY,
        authors TEXT,
        title TEXT,
        doi TEXT,
        abstract TEXT
    );
    '''
    cursor.execute(create_table_query)
    print("Table 'papers' created successfully.")


def insert_data_from_json(cursor, file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        arxiv_data = json.load(file)

        cnt = 0
        for entry in tqdm(arxiv_data, total=30000, desc="JSON to DB",
                                      unit=" lines"):
            authors = entry.get('authors', '')
            title = entry.get('title', '')
            doi = entry.get('doi', '')
            abstract = entry.get('abstract', '')

            insert_query = "INSERT INTO papers (authors, title, doi, abstract) VALUES (%s, %s, %s, %s);"
            record = (authors, title, doi, abstract)

            cursor.execute(insert_query, record)

            cnt += 1
            if cnt == 30000:
                break

        print("Data inserted into 'papers'.")


if __name__ == "__main__":
    try:
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(**db_params)

        # Create a cursor
        cursor = connection.cursor()

        # Create the 'papers' table
        create_papers_table(cursor)

        # Insert data from the JSON file
        json_file_path = 'arxiv_data.json'
        insert_data_from_json(cursor, json_file_path)

        # Commit the changes
        connection.commit()

    except Exception as e:
        print("Error:", e)

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()
