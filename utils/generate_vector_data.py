import numpy as np
import csv

# Generate vector data
vector_data = np.random.rand(1024).tolist()

# Save vector data to a CSV file
with open('vector_data.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(vector_data)
