import psycopg2
from flask import Flask, request
import socket

from psycopg2 import extras
from angle_emb import AnglE, Prompts

# Database connection parameters
db_params = {
    'host': 'postgres',
    'port': 5432,
    'database': 'arxiv_database',
    'user': 'arxiv_user',
    'password': 'arxiv_password',
}


def embed(model, txt):
    return model.encode({'text': txt}, to_numpy=True)


app = Flask(__name__)
angle = AnglE.from_pretrained('WhereIsAI/UAE-Large-V1',
                              pooling_strategy='cls')
angle.set_prompt(prompt=Prompts.C)


def return_data(text):
    emb = embed(angle, text)
    try:
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(**db_params)

        # Create a cursor with extras module
        cursor = connection.cursor(cursor_factory=extras.RealDictCursor)

        find_nearest_embedding_query = ("SELECT authors, title, abstract FROM papers "
                                        "ORDER BY encoded_abstract <-> %s::vector(1024) LIMIT 1;")
        cursor.execute(find_nearest_embedding_query, (emb.reshape(-1,).tolist(),))

        result = cursor.fetchone()
        if result:
            print("Authors:", result['authors'])
            print("Title:", result['title'])
            print("Abstract:", result['abstract'])
        else:
            print("No results found.")

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

    return result


@app.route('/', methods=['GET'])
def receive_data():
    print(socket.gethostname())
    try:
        data = request.args.to_dict()  # Assumes the client sends JSON data
        print("Received data:", data['query'])
        result = return_data(data['query'])
        result['status'] = 'success'
        result['host'] = socket.gethostname()
        return result
    except Exception as e:
        print("Error processing request:", e)
        return {'status': 'error', 'host': socket.gethostname()}


if __name__ == '__main__':
    app.run(debug=False)
