import requests
import time
from faker import Faker
from multiprocessing import Pool
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

server_url = 'http://localhost:80'
fake = Faker()

# Number of clients to simulate
NUM_CLIENTS = 10
NUM_QUERIES_PER_USER = 100


def send_query(user_id):
    user_start_time = time.time()
    individual_query_times = []

    for query_number in range(1, NUM_QUERIES_PER_USER + 1):
        query_start_time = time.time()

        # Simulate a query
        query_params = {'query': fake.paragraph(nb_sentences=2)}

        # Make a request to the server
        response = requests.get(f"{server_url}", params=query_params)
        
        query_time = time.time() - query_start_time

        individual_query_times.append(query_time)
        
    user_end_time = time.time()

    # Calculate mean time for individual queries
    mean_individual_query_time = sum(individual_query_times) / len(individual_query_times)
    logging.info(f"User {user_id}: Mean Time for Individual Query: {mean_individual_query_time:.4f} seconds")

    # Calculate overall time for the user
    user_total_time = user_end_time - user_start_time
    logging.info(f"User {user_id}: Total Time for All Queries: {user_total_time:.4f} seconds")

    return user_total_time


def main():
    # Create a pool of clients
    with Pool(processes=NUM_CLIENTS) as pool:
        # Map the client function to the pool
        query_times = pool.map(send_query, range(1, NUM_CLIENTS + 1))

    # Calculate the mean query time
    mean_user_time = sum(query_times) / len(query_times)
    print(f"Mean Time for All Users: {mean_user_time:.4f} seconds")


if __name__ == "__main__":
    main()
