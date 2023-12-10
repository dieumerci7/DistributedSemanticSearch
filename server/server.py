from flask import Flask, request
import socket


app = Flask(__name__)

@app.route('/', methods=['GET'])
def receive_data():
    print(socket.gethostname())
    try:
        data = request.args.to_dict()  # Assumes the client sends JSON data
        print("Received data:", data)
        return {'abstract': 'Cool abstract', 'hostname': str(socket.gethostname()), 'status': 'success'}
    except Exception as e:
        print("Error processing request:", e)
        return {'status': 'error'}

if __name__ == '__main__':
    app.run(debug = True)
