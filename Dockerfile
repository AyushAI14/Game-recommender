# Base image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /Game-recommender

# Copy necessary files into the container
COPY requirements.txt requirements.txt
COPY fasy.py fast.py
COPY model model
COPY Dataset Dataset
COPY templates templates
COPY static static
COPY Utility Utility

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the required port
EXPOSE 5000

# Set the default command to run the Flask app
CMD ["python", "fast.py"]
