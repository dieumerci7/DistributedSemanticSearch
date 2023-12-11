FROM python:3.9

# Set working directory
WORKDIR /server

# Copy application code to the container
COPY . /server

# Install dependencies (if any)
RUN pip install -r requirements.txt

# Command to run your server
CMD gunicorn --bind 0.0.0.0:5000 server:app --timeout 500
