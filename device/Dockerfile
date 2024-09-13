# Use the official Debian image
FROM debian:bullseye-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install Python and tesseract-ocr
RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN pip3 install --upgrade pip
RUN pip3 install openai
RUN pip3 install requests

# Set up a working directory
WORKDIR /device

# Copy application code
COPY . .

# Default command: drop into a bash shell
CMD ["/bin/bash"]
