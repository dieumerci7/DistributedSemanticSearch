import requests
import argparse

DEFAULT_IP = '127.0.0.1'
DEFAULT_PORT = 80

class ServerClient:
    def __init__(self, server_url):
        self.server_url = server_url

    def send_data_to_server(self, data):
        try:
            response = requests.get(self.server_url, params={'data': data})
            response_data = response.json()

            if response.status_code == 200 and response_data.get('status') == 'success':
                return response_data.get('abstract')
            else:
                return f"Error from server: {response_data.get('status')}"

        except Exception as e:
            return f"Error making request: {e}"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Client for interacting with the Flask server.')
    parser.add_argument('--ip', type=str, default=DEFAULT_IP, help='Server IP address')
    parser.add_argument('--port', type=int, default=DEFAULT_PORT, help='Server port')

    args = parser.parse_args()

    server_url = f'http://{args.ip}:{args.port}/'
    server_client = ServerClient(server_url)

    while True:
        user_input = input("Enter a string to send to the server (or 'exit' to end): ")

        if user_input.lower() == 'exit':
            break

        response = server_client.send_data_to_server(user_input)
        print("Server response:", response)
