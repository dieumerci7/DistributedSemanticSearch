FROM python:3.9

# Set working directory
WORKDIR /server

# Copy application code to the container
COPY . /server

# Install dependencies (if any)
RUN pip install -r requirements.txt

# Expose the port on which your server listens
EXPOSE 12345

# Command to run your server
CMD ["python", "server.py"]
