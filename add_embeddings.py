import psycopg2
import numpy as np
from tqdm import tqdm

# Database connection parameters
db_params = {
    'host': 'localhost',
    'port': 5432,
    'database': 'arxiv_database',
    'user': 'arxiv_user',
    'password': 'arxiv_password',
}


def load_encoded_abstracts(file_path):
    return np.load(file_path)


def add_column_and_update_data(cursor, encoded_abstracts):
    # Create the vector extension
    create_vector_extension_query = "CREATE EXTENSION IF NOT EXISTS vector;"
    cursor.execute(create_vector_extension_query)
    print("Vector extension created.")

    # Add a new column 'encoded_abstract' with type 'vector(1024)'
    add_column_query = "ALTER TABLE papers ADD COLUMN encoded_abstract VECTOR(1024);"
    cursor.execute(add_column_query)
    print("New column 'encoded_abstract' added to the 'papers' table.")

    # Update the 'encoded_abstract' column with values from the numpy array
    update_query = "UPDATE papers SET encoded_abstract = %s WHERE id = %s;"

    cnt = 0
    for i, encoded_abstract in tqdm(enumerate(encoded_abstracts), total=3000,
                                    desc="Add embeddings", unit=" lines"):
        cursor.execute(update_query, (encoded_abstract.reshape(-1,).tolist(), i + 1))
        cnt += 1
        if cnt == 3000:
            break

    print("Data updated in the 'encoded_abstract' column.")


if __name__ == "__main__":
    try:
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(**db_params)

        # Create a cursor
        cursor = connection.cursor()

        # Load the encoded abstracts from the numpy array
        npy_file_path = 'encoded_abstracts.npy'
        encoded_abstracts = load_encoded_abstracts(npy_file_path)

        # Add a new column to 'papers' and update data
        add_column_and_update_data(cursor, encoded_abstracts)

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
