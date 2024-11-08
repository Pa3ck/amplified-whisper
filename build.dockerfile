# Use a lightweight, compatible Python image (Python 3.9)
FROM --platform=linux/amd64 python:3.9-slim
# FROM --platform=linux/amd64 python:3.11-slim

# Set environment variables to prevent .pyc files, buffer logs, and force offline mode for transformers
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install necessary system dependencies (only what is required for the app)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 \
    && rm -rf /var/lib/apt/lists/*  # Clean up APT cache to reduce image size

# Set the working directory for the application
WORKDIR /

# Copy the requirements file into the image
COPY requirements.txt .

# Install gunicorn
RUN pip install gunicorn

# Install only the necessary Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install PyTorch and torchaudio (CPU version) from the PyTorch repository
# RUN pip install torch==2.5.1+cpu torchaudio --index-url https://download.pytorch.org/whl/cpu

# Install the Hugging Face transformers library
# RUN pip install transformers

# Copy the application code
COPY . .

# Expose the port that the Flask app will use
EXPOSE 8080

# Command to run the Flask app (using gunicorn for production)
CMD ["gunicorn", "-w", "9", "-b", "0.0.0.0:8080", "-k", "uvicorn.workers.UvicornWorker", "--timeout", "120", "server:app"]