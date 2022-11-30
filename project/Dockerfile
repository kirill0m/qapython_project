FROM python:3.10

WORKDIR /test_myapp

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .