FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y iproute2 && rm -rf /var/lib/apt/lists/*

COPY ip_tool.py /app/ip_tool.py

CMD ["python", "/app/ip_tool.py"]
