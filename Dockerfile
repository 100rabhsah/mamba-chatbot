# Use an official Python image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy project files
COPY requirements.txt .
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Install dependencies and Supervisor
RUN apt-get update && apt-get install -y supervisor && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expose API and Streamlit ports
EXPOSE 8000 8501

# Start Supervisor
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
