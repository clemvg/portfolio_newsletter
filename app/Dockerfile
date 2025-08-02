FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# The 'unbuffered' flag ensures that prints are sent straight to Cloud Run logs.
CMD ["python", "-u", "job_runner.py"]
