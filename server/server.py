import socket

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_address = ('0.0.0.0', 12345)
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(1)
print(f"Server is listening on {server_address}")

while True:
    # Wait for a connection
    print("Waiting for a connection...")
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address}")

    try:
        # Receive data from the client
        data = client_socket.recv(1024)
        print(f"Received data: {data.decode()}")

        # Send a response back to the client
        response = str(data) + " Messi > Ronaldo"
        client_socket.sendall(response.encode())
    finally:
        # Clean up the connection
        client_socket.close()
