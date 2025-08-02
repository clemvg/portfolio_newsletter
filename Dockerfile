FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/main.py .

# The 'unbuffered' flag ensures that prints are sent straight to Cloud Run logs.
CMD ["python", "-u", "main.py"]
