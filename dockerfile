FROM python:3.10.5

# Use absolute path
WORKDIR /usr/app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Create data directory with proper permissions
RUN mkdir -p /data && chmod 777 /data

# Copy rest of the application
COPY . .

CMD ["python3", "-u", "app.py"]