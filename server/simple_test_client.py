import requests


def send_data():
    url = 'http://localhost:80'
    data = {'query': 'graph theory'}
    try:
        response = requests.get(url, params=data)

        if response.status_code == 200:
            print("Data sent successfully")
            print(f"Response: {response.json()}")
        else:
            print("Failed to send data. Status code:", response.status_code)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    send_data()