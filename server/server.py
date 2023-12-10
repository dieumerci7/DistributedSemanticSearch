import json
import socket
from sklearn.metrics.pairwise import cosine_similarity
from embedding import embed

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_address = ('0.0.0.0', 12345)
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(1)
print(f"Server is listening on {server_address}")

with open('./server/proxy_db_updated.json', 'r') as file:
    db = json.load(file)

while True:
    # Wait for a connection
    print("Waiting for a connection...")
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address}")

    try:
        # Receive data from the client
        data = client_socket.recv(1024).decode()
        emb = embed(data)
        max_similarity = -2
        for item in db['articles']:
            # Calculate cosine similarity
            cosine_similarity_value = cosine_similarity(emb, item['vectorField'])[0, 0]
            if cosine_similarity_value >= max_similarity:
                max_similarity = cosine_similarity_value
                title = item['title']
                abstract = item['abstract']

        # Send a response back to the client
        response = f"Title: {title}\nAbstract: {abstract}"
        client_socket.sendall(response.encode())
    finally:
        # Clean up the connection
        client_socket.close()
