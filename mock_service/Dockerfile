FROM python:3.10

WORKDIR /mock_service

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .