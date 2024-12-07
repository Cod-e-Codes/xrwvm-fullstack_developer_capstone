FROM python:3.12.0-slim-bookworm
ENV PYTHONBUFFERED=1
ENV PYTHONWRITEBYTECODE=1
ENV APP=/app

# Set the working directory
WORKDIR $APP

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev

# Copy requirements and install Python dependencies
COPY requirements.txt $APP
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

# Copy the application files
COPY . $APP

# Expose port 8000
EXPOSE 8000

# Set permissions for entrypoint script
RUN chmod +x /app/entrypoint.sh

# Define the entrypoint and command to start the application
ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "djangoproj.wsgi"]
